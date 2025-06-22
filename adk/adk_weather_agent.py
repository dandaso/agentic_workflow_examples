import os
from weather_agent import WeatherAgent
from typing import Dict, Any
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio

class AdkWeatherAgent(WeatherAgent):
    """
    Google ADKを使った天気情報エージェントの実装
    """
    
    def __init__(self):
        super().__init__("Google ADK Weather Agent")
        
        # Gemini API キーの取得とバリデーション
        api_key = self._get_gemini_api_key()
        
        # Google ADKクライアントの初期化
        self.adk_client = self._initialize_adk_client()
    
    def _initialize_adk_client(self):
        """
        Google ADKクライアントを初期化（ツール付き）
        
        Returns:
            ADKクライアントインスタンス、または None（エラー時）
        """
        try:
            # ツール定義
            tools = self._create_adk_tools()
            
            # ADKエージェントの初期化（ツール付き）
            client = LlmAgent(
                name="weather_agent",
                model=self.GEMINI_MODEL,
                description="天気情報を提供するエージェント",
                tools=tools,
                instruction="""
                あなたは天気情報を提供する親切なアシスタントです。
                ユーザーから都市名を受け取り、その都市の天気情報を日本語で分かりやすく説明してください。
                
                利用可能なツール:
                - get_city_coordinates: 都市名から地理座標を取得
                - get_weather_data: 座標から詳細な天気情報を取得
                
                手順:
                1. get_city_coordinatesツールを使って都市の座標を取得
                2. get_weather_dataツールを使って座標から天気情報を取得  
                3. 取得した情報を分かりやすく日本語で説明
                """
            )
            return client
                
        except Exception as e:
            print(f"ADK初期化エラー: {e}")
            return None
    
    def _create_adk_tools(self):
        """
        ADK用のツールを作成
        
        Returns:
            ツールのリスト
        """
        def get_city_coordinates(city: str) -> Dict[str, float]:
            """
            都市名から地理座標（緯度・経度）を取得します。
            
            Args:
                city: 都市名（例: "東京", "大阪", "New York"）
                
            Returns:
                座標辞書 {"lat": 緯度, "lng": 経度}
            """
            return self._get_coordinates_real(city)
        
        def get_weather_data(lat: float, lng: float) -> Dict[str, Any]:
            """
            座標から詳細な天気情報を取得します。
            
            Args:
                lat: 緯度
                lng: 経度
                
            Returns:
                天気データ辞書
            """
            return self._get_weather_data_real(lat, lng)
        
        # FunctionToolとして作成
        coord_tool = FunctionTool(get_city_coordinates)
        weather_tool = FunctionTool(get_weather_data)
        
        return [coord_tool, weather_tool]

    def run(self, city: str) -> str:
        """
        Google ADKを使って指定された都市の天気情報を取得
        
        Args:
            city: 都市名
            
        Returns:
            天気情報を含む日本語メッセージ
            
        Raises:
            Exception: ADKクライアントが初期化されていない場合やその他のエラー
        """
        try:
            return asyncio.run(self._run_async(city))
        except Exception as e:
            error_msg = f"天気情報の取得中にエラーが発生しました: {e}"
            print(error_msg)
            return f"[{self.name}] {error_msg}"

    async def _run_async(self, city: str) -> str:
        runner = Runner(
            agent=self.adk_client,
            session_service=InMemorySessionService(),
            app_name="weather_agent"
        )
        query = f"{city}の天気を教えてください"
        content = types.Content(role='user', parts=[types.Part(text=query)])
        await runner.session_service.create_session(app_name="weather_agent", user_id="cli_user", session_id="cli_session")
        
        response = ""
        async for event in runner.run_async(user_id="cli_user", session_id="cli_session", new_message=content):
            if event.is_final_response() and event.content and event.content.parts:
                response = event.content.parts[0].text
                break
        return response

