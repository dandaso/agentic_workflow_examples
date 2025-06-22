import os
from weather_agent import WeatherAgent
from typing import List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
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
        
        # プロンプトテンプレートの設定
        prompt_template = PromptTemplate.from_template("""
あなたは天気情報を提供する親切なアシスタントです。
ユーザーから都市名を受け取り、その都市の天気情報を日本語で分かりやすく説明してください。

質問: {input}
""")
        
        self.chain = prompt_template | self.llm
        
        # ツール定義（後で実装）
        self.tools = self._create_tools()
    
    def _create_tools(self) -> List[Any]:
        """
        LangChain用のツールを作成
        """
        # 基本的なツール定義（後で拡張）
        tools = []
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
            # LangChain LLMチェーンを使って天気情報を取得
            prompt = f"{city}の天気情報を教えてください。"
            
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