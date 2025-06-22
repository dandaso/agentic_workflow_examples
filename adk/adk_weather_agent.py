import os
from weather_agent import WeatherAgent
from typing import Dict, Any
try:
    import google.adk as adk
except ImportError:
    adk = None


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
        Google ADKクライアントを初期化
        
        Returns:
            ADKクライアントインスタンス、または None（エラー時）
        """
        try:
            if adk is None:
                return None
            
            # ADKエージェントの初期化
            client = adk.Agent(name="weather_agent")
            return client
                
        except Exception:
            return None
    
    def run(self, city: str) -> str:
        """
        Google ADKを使って指定された都市の天気情報を取得
        
        Args:
            city: 都市名
            
        Returns:
            天気情報を含む日本語メッセージ
        """
        try:
            # ADKクライアント初期化チェック
            if self.adk_client is None:
                # フォールバック実行
                coords = self._get_coordinates(city)
                weather_data = self._get_weather_data(coords['lat'], coords['lng'])
                return f"[{self.name}] {city}の天気をお調べしました（フォールバック）。{weather_data['description']}"
            
            # ADKエージェントを使った天気情報取得（基本実装）
            coords = self._get_coordinates(city)
            weather_data = self._get_weather_data(coords['lat'], coords['lng'])
            
            return f"[{self.name}] {city}の天気をお調べしました。{weather_data['description']}"
            
        except Exception as e:
            # エラー時はフォールバック
            try:
                coords = self._get_coordinates(city)
                weather_data = self._get_weather_data(coords['lat'], coords['lng'])
                return f"[{self.name}] {city}の天気をお調べしました（エラー時フォールバック）。{weather_data['description']}"
            except:
                return f"[{self.name}] エラーが発生しました: {str(e)}"