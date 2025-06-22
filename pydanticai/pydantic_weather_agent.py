import os
from weather_agent import WeatherAgent
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.gemini import GeminiModel
import googlemaps
import requests
from typing import Optional, Dict


class PydanticWeatherAgent(WeatherAgent):
    """
    PydanticAIを使った天気情報エージェントの実装
    """
    
    def __init__(self):
        super().__init__("PydanticAI Weather Agent")
        
        # Geminiモデルの設定（API キーを環境変数から自動取得）
        api_key = self._get_gemini_api_key()  # バリデーションのため
        self.model = GeminiModel(self.GEMINI_MODEL)
        
        # PydanticAI Agentの初期化（ツール付き）
        self.agent = Agent(
            model=self.model,
            tools=[self.__get_city_coordinates],
            system_prompt="""
            あなたは天気情報を提供する親切なアシスタントです。
            ユーザーから都市名を受け取り、その都市の天気情報を日本語で分かりやすく説明してください。
            
            利用可能なツール:
            - __get_city_coordinates: 都市名から緯度・経度を取得
            
            手順:
            1. まず __get_city_coordinates ツールを使って都市の座標を取得
            2. その座標情報を元に天気情報を説明
            """,
        )
    
    def __get_city_coordinates(self, city: str) -> Dict[str, float]:
        """
        都市名から地理座標を取得するプライベートツール
        
        Args:
            city: 都市名
            
        Returns:
            座標辞書 {"lat": 緯度, "lng": 経度}
        """
        try:
            return self._get_coordinates_real(city)
        except Exception as e:
            # エラー時はフォールバック（東京の座標）
            print(f"ジオコーディングエラー: {e}")
            return {"lat": 35.6762, "lng": 139.6503}
    
    def run(self, city: str) -> str:
        """
        PydanticAIを使って指定された都市の天気情報を取得
        
        Args:
            city: 都市名
            
        Returns:
            天気情報を含む日本語メッセージ
        """
        try:
            # PydanticAI Agentを使ってツール連携で天気情報を取得
            prompt = f"""
            {city}の天気情報を教えてください。
            
            手順:
            1. __get_city_coordinates ツールを使って {city} の緯度・経度を取得してください
            2. 取得した座標情報と模擬的な天気データを組み合わせて、ユーザーに分かりやすく説明してください
            """
            
            result = self.agent.run_sync(prompt)
            return f"[{self.name}] {result.data}"
            
        except Exception as e:
            return f"[{self.name}] エラーが発生しました: {str(e)}"