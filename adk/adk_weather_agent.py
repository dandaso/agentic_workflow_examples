from weather_agent import WeatherAgent


class AdkWeatherAgent(WeatherAgent):
    """
    Google ADKを使った天気情報エージェントの実装
    """
    
    def __init__(self):
        super().__init__("ADK Weather Agent")
    
    def run(self, city: str) -> str:
        """
        Google ADKを使って指定された都市の天気情報を取得
        
        Args:
            city: 都市名
            
        Returns:
            天気情報を含む日本語メッセージ
        """
        # 座標を取得
        coords = self._get_coordinates(city)
        
        # 天気データを取得
        weather_data = self._get_weather_data(coords['lat'], coords['lng'])
        
        # ADKエージェントからのメッセージとして返す
        return f"[{self.name}] {city}の天気をお調べしました。{weather_data['description']}"