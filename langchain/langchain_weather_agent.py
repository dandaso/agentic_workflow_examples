import os
from weather_agent import WeatherAgent
from typing import List, Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
import langchain
langchain.verbose = False
langchain.debug = False
langchain.llm_cache = False


class LangchainWeatherAgent(WeatherAgent):
    """
    LangChainを使った天気情報エージェントの実装
    """
    
    def __init__(self):
        super().__init__("LangChain Weather Agent")
        
        # Geminiモデルの設定（API キーを環境変数から自動取得）
        api_key = self._get_gemini_api_key()  # バリデーションのため
        
        # 環境変数を直接設定
        os.environ['GOOGLE_API_KEY'] = api_key
        
        # LangChain LLMの初期化
        self.llm = ChatGoogleGenerativeAI(
            model=self.GEMINI_MODEL,
            temperature=0.7
        )
        
        # ツール定義
        self.tools = self._create_tools()
        
        # プロンプトテンプレートの設定
        prompt_template = PromptTemplate.from_template("""
あなたは天気情報を提供する親切なアシスタントです。
ユーザーから都市名を受け取り、その都市の天気情報を日本語で分かりやすく説明してください。

質問: {input}
""")
        
        self.chain = prompt_template | self.llm
    
    def _create_tools(self) -> List[Any]:
        """
        LangChain用のツールを作成
        """
        @tool
        def get_city_coordinates(city: str) -> Dict[str, float]:
            """
            都市名から地理座標（緯度・経度）を取得します。
            
            Args:
                city: 都市名（例: "東京", "大阪", "New York"）
                
            Returns:
                座標辞書 {"lat": 緯度, "lng": 経度}
            """
            try:
                return self._get_coordinates_real(city)
            except Exception as e:
                print(f"ジオコーディングエラー: {e}")
                # エラー時はフォールバック（東京の座標）
                return {"lat": 35.6762, "lng": 139.6503}
        
        tools = [get_city_coordinates]
        return tools
    
    def run(self, city: str) -> str:
        """
        LangChainを使って指定された都市の天気情報を取得
        
        Args:
            city: 都市名
            
        Returns:
            天気情報を含む日本語メッセージ
        """
        try:
            # ツールを使って座標を取得
            get_city_coordinates_tool = self.tools[0]  # get_city_coordinates tool
            coords = get_city_coordinates_tool.invoke(city)
            
            # LLMに座標情報を含めて質問
            prompt = f"{city}の天気情報を教えてください。この都市の座標は緯度{coords['lat']}度、経度{coords['lng']}度です。"
            
            result = self.chain.invoke({"input": prompt})
            return f"[{self.name}] {result.content}"
            
        except Exception as e:
            # エラー時はフォールバック
            try:
                coords = self._get_coordinates(city)
                weather_data = self._get_weather_data(coords['lat'], coords['lng'])
                return f"[{self.name}] {city}の天気をお調べしました（フォールバック）。{weather_data['description']}"
            except:
                return f"[{self.name}] エラーが発生しました: {str(e)}"