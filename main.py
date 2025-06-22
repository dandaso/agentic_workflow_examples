def get_city_input():
    """ユーザーから都市名を入力してもらう"""
    city = input("天気を知りたい都市名を入力してください: ")
    return city

def mock_geocoding(city):
    """Google Maps Geocoding APIのモック"""
    mock_data = {
        "東京": {"lat": 35.6762, "lng": 139.6503},
        "大阪": {"lat": 34.6937, "lng": 135.5023},
        "名古屋": {"lat": 35.1815, "lng": 136.9066},
        "札幌": {"lat": 43.0642, "lng": 141.3469},
        "福岡": {"lat": 33.5904, "lng": 130.4017}
    }
    return mock_data.get(city, {"lat": 35.6762, "lng": 139.6503})

def mock_weather_api(lat, lng):
    """OpenWeatherMap APIのモック"""
    import random
    weather_conditions = ["晴れ", "曇り", "雨", "雪", "霧"]
    temperature = random.randint(-5, 35)
    condition = random.choice(weather_conditions)
    
    return {
        "temperature": temperature,
        "condition": condition,
        "description": f"気温は{temperature}度、天気は{condition}です。"
    }

def display_weather(city, weather_data):
    """天気情報を日本語で出力"""
    print(f"\n{city}の天気情報:")
    print(f"- {weather_data['description']}")

def main():
    print("天気情報アプリへようこそ！")
    
    # 都市名を入力
    city = get_city_input()
    
    # 経度緯度を取得（モック）
    coords = mock_geocoding(city)
    print(f"{city}の座標: 緯度{coords['lat']}, 経度{coords['lng']}")
    
    # 天気情報を取得（モック）
    weather = mock_weather_api(coords['lat'], coords['lng'])
    
    # 天気情報を表示
    display_weather(city, weather)
    
    print("\nありがとうございました！")


if __name__ == "__main__":
    main()
