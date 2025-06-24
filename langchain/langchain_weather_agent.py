import os

from weather_agent import WeatherAgent
from typing import List, Any, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
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
        
        # 環境変数を直接設定（langchain_google_genaiはGOOGLE_API_KEYを使用）
        os.environ['GOOGLE_API_KEY'] = api_key
        
        # LangChain LLMの初期化（ツール呼び出し機能を有効化）
        self.llm = ChatGoogleGenerativeAI(
            model=self.GEMINI_MODEL,
            temperature=0.7
        )
        
        # ツール定義
        self.tools = self._create_tools()
        
        # ReActエージェントを作成（LLMが自動的にツールを選択・実行）
        self.agent_executor = create_react_agent(self.llm, self.tools)
    
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
        
        @tool
        def get_weather_data(lat: float, lng: float) -> Dict[str, Any]:
            """
            座標から詳細な天気情報を取得します。
            
            Args:
                lat: 緯度
                lng: 経度
                
            Returns:
                天気データ辞書
            """
            try:
                return self._get_weather_data_real(lat, lng)
            except Exception as e:
                print(f"天気APIエラー: {e}")
                # エラー時はフォールバック（モックデータ）
                return self._get_weather_data(lat, lng)
        
        tools = [get_city_coordinates, get_weather_data]
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
            # エージェントにタスクを実行させる
            result = self.agent_executor.invoke({
                "messages": [{
                    "role": "user",
                    "content": f"""
あなたは天気情報を提供する親切なアシスタントです。
{city}の天気情報を教えてください。

手順:
1. まず get_city_coordinates ツールを使って都市の座標を取得してください
2. 次に get_weather_data ツールを使って座標から天気情報を取得してください
3. 取得した情報を分かりやすく日本語で説明してください
"""
                }]
            })
            
            # 最終メッセージを取得
            final_message = result["messages"][-1]
            return f"[{self.name}] {final_message.content}"
            
        except Exception as e:
            # エラー時はフォールバック
            try:
                coords = self._get_coordinates(city)
                weather_data = self._get_weather_data(coords['lat'], coords['lng'])
                return f"[{self.name}] {city}の天気をお調べしました（フォールバック）。{weather_data['description']}"
            except:
                return f"[{self.name}] エラーが発生しました: {str(e)}"