from abc import ABC, abstractmethod
from typing import Dict, Any


class WeatherAgent(ABC):
    """
    天気情報を取得するエージェントの共通インターフェース
    各ライブラリ（ADK, PydanticAI, LangChain）で実装される
    """
    
    # 共通のGeminiモデル名
    GEMINI_MODEL = 'gemini-1.5-flash'
    
    def __init__(self, name: str):
        """
        Args:
            name: エージェントの名前
        """
        self.name = name
    
    @abstractmethod
    def run(self, city: str) -> str:
        """
        指定された都市の天気情報を取得して日本語メッセージを返す
        
        Args:
            city: 都市名
            
        Returns:
            天気情報を含む日本語メッセージ
        """
        pass
    
    def get_name(self) -> str:
        """エージェント名を返す"""
        return self.name
    
    def _get_coordinates(self, city: str) -> Dict[str, float]:
        """
        都市名から座標を取得する共通メソッド（モック）
        サブクラスでオーバーライド可能
        """
        mock_data = {
            "東京": {"lat": 35.6762, "lng": 139.6503},
            "大阪": {"lat": 34.6937, "lng": 135.5023},
            "名古屋": {"lat": 35.1815, "lng": 136.9066},
            "札幌": {"lat": 43.0642, "lng": 141.3469},
            "福岡": {"lat": 33.5904, "lng": 130.4017}
        }
        return mock_data.get(city, {"lat": 35.6762, "lng": 139.6503})
    
    def _get_weather_data(self, lat: float, lng: float) -> Dict[str, Any]:
        """
        座標から天気データを取得する共通メソッド（モック）
        サブクラスでオーバーライド可能
        """
        import random
        weather_conditions = ["晴れ", "曇り", "雨", "雪", "霧"]
        temperature = random.randint(-5, 35)
        condition = random.choice(weather_conditions)
        
        return {
            "temperature": temperature,
            "condition": condition,
            "description": f"気温は{temperature}度、天気は{condition}です。"
        }