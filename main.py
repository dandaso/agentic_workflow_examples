from dotenv import load_dotenv
import sys
from typing import Optional
from weather_agent import WeatherAgent

# 環境変数を読み込み
load_dotenv()

def show_menu():
    """ライブラリ選択メニューを表示"""
    print("=" * 50)
    print("🌤️  Weather Agent Workflow Examples")
    print("=" * 50)
    print()
    print("使用するライブラリを選択してください：")
    print()
    print("1️⃣  Google ADK")
    print("   - Google Agent Development Kit")
    print("   - LlmAgentとRunnerによる実行")
    print()
    print("2️⃣  LangChain")
    print("   - LangChain AgentExecutor")
    print("   - ツールとプロンプトによる実行")
    print()
    print("3️⃣  PydanticAI")
    print("   - Pydantic AI Agent")
    print("   - 型安全なエージェント実行")
    print()
    print("0️⃣  終了")
    print()

def get_library_choice() -> str:
    """ユーザーからライブラリ選択を取得"""
    while True:
        choice = input("選択 (0-3): ").strip()
        if choice in ['0', '1', '2', '3']:
            return choice
        print("❌ 無効な選択です。0-3の数字を入力してください。")

def create_agent(choice: str) -> Optional[WeatherAgent]:
    """選択されたライブラリのエージェントを作成"""
    try:
        if choice == '1':
            from adk.adk_weather_agent import AdkWeatherAgent
            print("\n🚀 Google ADK Weather Agentを初期化中...")
            return AdkWeatherAgent()
        
        elif choice == '2':
            from langchain.langchain_weather_agent import LangchainWeatherAgent
            print("\n🚀 LangChain Weather Agentを初期化中...")
            return LangchainWeatherAgent()
        
        elif choice == '3':
            from pydanticai.pydantic_weather_agent import PydanticWeatherAgent
            print("\n🚀 PydanticAI Weather Agentを初期化中...")
            return PydanticWeatherAgent()
        
        return None
        
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("必要な依存関係がインストールされていない可能性があります。")
        return None
    except ValueError as e:
        print(f"❌ 設定エラー: {e}")
        print("必要な環境変数（API キー）が設定されていない可能性があります。")
        return None
    except Exception as e:
        print(f"❌ 初期化エラー: {e}")
        return None

def get_city_input() -> str:
    """ユーザーから都市名を入力してもらう"""
    print()
    while True:
        city = input("🌍 天気を知りたい都市名を入力してください: ").strip()
        if city:
            return city
        print("❌ 都市名を入力してください。")

def run_weather_agent(agent: WeatherAgent, city: str):
    """エージェントを実行して天気情報を取得"""
    print(f"\n🔍 {city}の天気情報を取得中...")
    print("-" * 30)
    
    try:
        result = agent.run(city)
        print(f"\n✅ {result}")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("API キーの設定やネットワーク接続を確認してください。")

def main():
    """メイン実行関数"""
    try:
        while True:
            show_menu()
            choice = get_library_choice()
            
            if choice == '0':
                print("\n👋 ご利用ありがとうございました！")
                sys.exit(0)
            
            # エージェントを作成
            agent = create_agent(choice)
            if agent is None:
                print("\n⚠️  エージェントの初期化に失敗しました。メニューに戻ります。")
                input("\nEnterキーを押して続行...")
                continue
            
            print(f"✅ {agent.name} の初期化が完了しました。")
            
            # 都市名を入力
            city = get_city_input()
            
            # 天気情報を取得
            run_weather_agent(agent, city)
            
            # 続行確認
            print()
            while True:
                continue_choice = input("🔄 別の検索を行いますか？ (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("\n👋 ご利用ありがとうございました！")
                    sys.exit(0)
                else:
                    print("❌ 'y' または 'n' を入力してください。")
    
    except KeyboardInterrupt:
        print("\n\n👋 プログラムを終了します。")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
