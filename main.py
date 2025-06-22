from dotenv import load_dotenv
from adk.adk_weather_agent import AdkWeatherAgent

# 環境変数を読み込み
load_dotenv()

def get_city_input():
    """ユーザーから都市名を入力してもらう"""
    city = input("天気を知りたい都市名を入力してください: ")
    return city

def main():
    print("天気情報アプリへようこそ！")
    
    # Google ADK Weather Agentを初期化
    agent = AdkWeatherAgent()
    
    # 都市名を入力
    city = get_city_input()
    
    # エージェントで天気情報を取得
    result = agent.run(city)
    
    # 結果を表示
    print(f"\n{result}")
    
    print("\nありがとうございました！")


if __name__ == "__main__":
    main()
