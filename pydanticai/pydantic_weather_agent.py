import os
from weather_agent import WeatherAgent
from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
import googlemaps
import requests
from typing import Optional


class PydanticWeatherAgent(WeatherAgent):
    """
    PydanticAIを使った天気情報エージェントの実装
    """
    
    def __init__(self):
        super().__init__("PydanticAI Weather Agent")
        
        # Geminiモデルの設定（API キーを環境変数に設定済みの前提）
        api_key = self._get_gemini_api_key()  # バリデーションのため
        self.model = GeminiModel(self.GEMINI_MODEL)
        
        # PydanticAI Agentの初期化
        self.agent = Agent(
            model=self.model,
            system_prompt="""
            あなたは天気情報を提供する親切なアシスタントです。
            ユーザーから都市名を受け取り、その都市の天気情報を日本語で分かりやすく説明してください。
            """,
        )
    
    def run(self, city: str) -> str:
        """
        PydanticAIを使って指定された都市の天気情報を取得
        
        Args:
            city: 都市名
            
        Returns:
            天気情報を含む日本語メッセージ
        """
        try:
            # 基本的なrun_syncの実装（まずはモック）
            coords = self._get_coordinates(city)
            weather_data = self._get_weather_data(coords['lat'], coords['lng'])
            
            # PydanticAI Agentを使って自然な日本語で回答生成
            prompt = f"""
            {city}の天気情報をお伝えします。
            座標: 緯度{coords['lat']}, 経度{coords['lng']}
            天気: {weather_data['condition']}
            気温: {weather_data['temperature']}度
            
            この情報を使って、ユーザーに分かりやすく天気を説明してください。
            """
            
            result = self.agent.run_sync(prompt)
            return f"[{self.name}] {result.data}"
            
        except Exception as e:
            return f"[{self.name}] エラーが発生しました: {str(e)}"