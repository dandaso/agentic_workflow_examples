import os
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
    
    def _get_gemini_api_key(self) -> str:
        """
        Gemini API キーを環境変数から取得する共通メソッド
        
        Returns:
            API キー文字列
            
        Raises:
            ValueError: API キーが設定されていない場合
        """
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY環境変数が設定されていません")
        return api_key
    
    def _get_google_maps_api_key(self) -> str:
        """
        Google Maps API キーを環境変数から取得する共通メソッド
        
        Returns:
            API キー文字列
            
        Raises:
            ValueError: API キーが設定されていない場合
        """
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY環境変数が設定されていません")
        return api_key
    
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
    
    def _get_coordinates_real(self, city: str) -> Dict[str, float]:
        """
        都市名から座標を取得する実装（Google Maps Geocoding API使用）
        
        Args:
            city: 都市名
            
        Returns:
            座標辞書 {"lat": 緯度, "lng": 経度}
            
        Raises:
            ValueError: 都市が見つからない場合
            Exception: API呼び出しエラーの場合
        """
        import googlemaps
        
        try:
            api_key = self._get_google_maps_api_key()
            gmaps = googlemaps.Client(key=api_key)
            
            # ジオコーディング実行
            geocode_result = gmaps.geocode(city)
            
            if not geocode_result:
                raise ValueError(f"都市 '{city}' が見つかりませんでした")
            
            # 最初の結果から座標を取得
            location = geocode_result[0]['geometry']['location']
            return {
                "lat": location['lat'],
                "lng": location['lng']
            }
            
        except ValueError:
            raise  # 都市が見つからない場合はそのまま再発生
        except Exception as e:
            raise Exception(f"ジオコーディングAPIエラー: {str(e)}")
    
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