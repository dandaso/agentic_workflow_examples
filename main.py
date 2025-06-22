from dotenv import load_dotenv
import sys
from cli import WeatherAgentCLI

# 環境変数を読み込み
load_dotenv()


def run():
    """CLIのメインループを実行"""
    cli = WeatherAgentCLI()
    
    try:
        while True:
            cli.show_menu()
            choice = cli.get_library_choice()
            
            if choice == '0':
                print("\n👋 ご利用ありがとうございました！")
                break
            
            # エージェントを作成
            agent = cli.create_agent(choice)
            if agent is None:
                print("\n⚠️  エージェントの初期化に失敗しました。メニューに戻ります。")
                input("\nEnterキーを押して続行...")
                continue
            
            print(f"✅ {agent.name} の初期化が完了しました。")
            
            # 都市名を入力
            city = cli.get_city_input()
            
            # 天気情報を取得
            cli.run_weather_agent(agent, city)
            
            # 続行確認
            if not cli.ask_continue():
                print("\n👋 ご利用ありがとうございました！")
                break
    
    except KeyboardInterrupt:
        print("\n\n👋 プログラムを終了します。")
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        sys.exit(1)


def main():
    """メイン実行関数 - CLIを起動"""
    run()


if __name__ == "__main__":
    main()
