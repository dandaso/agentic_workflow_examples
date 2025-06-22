import sys
from typing import Optional
from weather_agent import WeatherAgent


class WeatherAgentCLI:
    """
    天気エージェントのCLIインターフェース
    ライブラリ選択とエージェント実行を管理
    """
    
    def __init__(self):
        """CLIインスタンスを初期化"""
        self.library_options = {
            '1': {
                'name': 'Google ADK',
                'description': 'Google Agent Development Kit',
                'details': 'LlmAgentとRunnerによる実行',
                'module': 'adk.adk_weather_agent',
                'class': 'AdkWeatherAgent'
            },
            '2': {
                'name': 'LangChain',
                'description': 'LangChain AgentExecutor',
                'details': 'ツールとプロンプトによる実行',
                'module': 'langchain.langchain_weather_agent',
                'class': 'LangchainWeatherAgent'
            },
            '3': {
                'name': 'PydanticAI',
                'description': 'Pydantic AI Agent',
                'details': '型安全なエージェント実行',
                'module': 'pydanticai.pydantic_weather_agent',
                'class': 'PydanticWeatherAgent'
            }
        }
    
    def show_menu(self):
        """ライブラリ選択メニューを表示"""
        print("=" * 50)
        print("🌤️  Weather Agent Workflow Examples")
        print("=" * 50)
        print()
        print("使用するライブラリを選択してください：")
        print()
        
        for choice, info in self.library_options.items():
            print(f"{choice}️⃣  {info['name']}")
            print(f"   - {info['description']}")
            print(f"   - {info['details']}")
            print()
        
        print("0️⃣  終了")
        print()
    
    def get_library_choice(self) -> str:
        """ユーザーからライブラリ選択を取得"""
        valid_choices = list(self.library_options.keys()) + ['0']
        while True:
            choice = input("選択 (0-3): ").strip()
            if choice in valid_choices:
                return choice
            print("❌ 無効な選択です。0-3の数字を入力してください。")
    
    def create_agent(self, choice: str) -> Optional[WeatherAgent]:
        """選択されたライブラリのエージェントを作成"""
        if choice not in self.library_options:
            return None
        
        option = self.library_options[choice]
        
        try:
            print(f"\n🚀 {option['name']} Weather Agentを初期化中...")
            
            # 動的インポート
            module = __import__(option['module'], fromlist=[option['class']])
            agent_class = getattr(module, option['class'])
            
            return agent_class()
            
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
    
    def get_city_input(self) -> str:
        """ユーザーから都市名を入力してもらう"""
        print()
        while True:
            city = input("🌍 天気を知りたい都市名を入力してください: ").strip()
            if city:
                return city
            print("❌ 都市名を入力してください。")
    
    def run_weather_agent(self, agent: WeatherAgent, city: str):
        """エージェントを実行して天気情報を取得"""
        print(f"\n🔍 {city}の天気情報を取得中...")
        print("-" * 30)
        
        try:
            result = agent.run(city)
            print(f"\n✅ {result}")
            
        except Exception as e:
            print(f"\n❌ エラーが発生しました: {e}")
            print("API キーの設定やネットワーク接続を確認してください。")
    
    def ask_continue(self) -> bool:
        """続行するかユーザーに確認"""
        print()
        while True:
            continue_choice = input("🔄 別の検索を行いますか？ (y/n): ").strip().lower()
            if continue_choice in ['y', 'yes']:
                return True
            elif continue_choice in ['n', 'no']:
                return False
            else:
                print("❌ 'y' または 'n' を入力してください。")