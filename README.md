# 🌤️ Weather Agent Workflow Examples

3つの主要なPython Agentライブラリ（Google ADK、LangChain、PydanticAI）を使用した天気情報取得エージェントのサンプル実装プロジェクトです。

## 📋 プロジェクト概要

このプロジェクトは、Pythonで利用可能な主要なAgenticワークフローライブラリを使って、同じ機能（天気情報取得）を実装することで、各ライブラリの特徴と使い方を学習できるサンプル集です。

### 🎯 主な機能

- **ライブラリ選択**: CLI起動時に使用するライブラリを選択
- **天気情報取得**: 都市名から現在の天気情報を取得
- **統一インターフェース**: 全ライブラリで共通のWeatherAgentクラスを使用
- **エラーハンドリング**: 包括的なエラー処理とユーザーフレンドリーなメッセージ

### 🛠️ 対応ライブラリ

1. **Google ADK** - Google Agent Development Kit
   - LlmAgentとRunnerによる実行
   - FunctionToolを使用したツール統合

2. **LangChain** - LangChain AgentExecutor  
   - ツールとプロンプトによる実行
   - AgentExecutorでのワークフロー管理

3. **PydanticAI** - Pydantic AI Agent
   - 型安全なエージェント実行
   - Pydanticモデルによるデータ検証

## 🚀 セットアップ

### 前提条件

- Python 3.8以上
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー

### 1. リポジトリのクローン

```bash
git clone https://github.com/dandaso/agentic_workflow_examples.git
cd agentic_workflow_examples
```

### 2. 依存関係のインストール

```bash
uv sync
```

これにより、全ライブラリの依存関係が自動的にインストールされます。

### 3. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、以下のAPIキーを設定してください：

```bash
# .env ファイル
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

#### APIキーの取得方法

**Gemini API キー:**
1. [Google AI Studio](https://makersuite.google.com/) にアクセス
2. 「Get API key」をクリック
3. 新しいAPIキーを作成

**Google Maps API キー:**
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. プロジェクトを作成または選択
3. APIs & Services > Credentials で API キーを作成
4. Geocoding API を有効化

## 🎮 使い方

### CLI起動

```bash
uv run python main.py
```

### 使用手順

1. **ライブラリ選択**
   ```
   🌤️  Weather Agent Workflow Examples
   ==================================================
   
   使用するライブラリを選択してください：
   
   1️⃣  Google ADK
      - Google Agent Development Kit
      - LlmAgentとRunnerによる実行
   
   2️⃣  LangChain
      - LangChain AgentExecutor
      - ツールとプロンプトによる実行
   
   3️⃣  PydanticAI
      - Pydantic AI Agent
      - 型安全なエージェント実行
   
   0️⃣  終了
   
   選択 (0-3): 1
   ```

2. **エージェント初期化**
   ```
   🚀 Google ADK Weather Agentを初期化中...
   ✅ Google ADK Weather Agent の初期化が完了しました。
   ```

3. **都市名入力**
   ```
   🌍 天気を知りたい都市名を入力してください: 東京
   ```

4. **天気情報取得**
   ```
   🔍 東京の天気情報を取得中...
   ------------------------------
   
   ✅ [Google ADK Weather Agent] 東京の現在の天気: 気温25°C、晴れです。
   ```

5. **続行確認**
   ```
   🔄 別の検索を行いますか？ (y/n): n
   👋 ご利用ありがとうございました！
   ```

## 📁 プロジェクト構造

```
agentic_workflow_examples/
├── README.md                    # このファイル
├── main.py                      # メインエントリーポイント
├── cli.py                       # CLIインターフェースクラス
├── weather_agent.py             # 共通ベースクラス
├── adk/                         # Google ADK実装
│   ├── __init__.py
│   └── adk_weather_agent.py
├── langchain/                   # LangChain実装
│   ├── __init__.py
│   └── langchain_weather_agent.py
├── pydanticai/                  # PydanticAI実装
│   ├── __init__.py
│   └── pydantic_weather_agent.py
├── pyproject.toml               # プロジェクト設定
├── uv.lock                      # 依存関係ロック
└── .env                         # 環境変数（要作成）
```

## 🔧 開発者向け情報

### 新しいライブラリの追加

1. `weather_agent.py` の `WeatherAgent` クラスを継承
2. `run(self, city: str) -> str` メソッドを実装
3. `cli.py` の `library_options` に新しいエントリを追加

### カスタマイズ

各エージェントは独立しているため、必要に応じて個別にカスタマイズできます：

- **Google ADK**: `adk/adk_weather_agent.py`
- **LangChain**: `langchain/langchain_weather_agent.py`  
- **PydanticAI**: `pydanticai/pydantic_weather_agent.py`

## 🛠️ トラブルシューティング

### よくある問題

**1. インポートエラー**
```
❌ インポートエラー: No module named 'google.adk'
```
**解決方法**: `uv sync` で依存関係を再インストール

**2. API キー設定エラー**
```
❌ 設定エラー: GEMINI_API_KEY環境変数が設定されていません
```
**解決方法**: `.env` ファイルでAPI キーを設定

**3. ネットワークエラー**
```
❌ エラーが発生しました: API呼び出しに失敗しました
```
**解決方法**: 
- インターネット接続を確認
- API キーが有効か確認
- API制限に達していないか確認

### デバッグモード

より詳細なログが必要な場合：

```bash
# 環境変数でデバッグモードを有効化
export DEBUG=1
uv run python main.py
```

## 📚 各ライブラリについて

### Google ADK
- **特徴**: Googleが開発したエージェント開発キット
- **適用場面**: エンタープライズ環境、複雑なワークフロー
- **学習リソース**: [Google ADK Documentation](https://google.github.io/adk-docs/)

### LangChain
- **特徴**: 最も人気のあるLLMアプリケーション開発フレームワーク
- **適用場面**: プロトタイプ開発、豊富なツール統合
- **学習リソース**: [LangChain Documentation](https://python.langchain.com/)

### PydanticAI
- **特徴**: 型安全性を重視した新世代エージェントフレームワーク
- **適用場面**: 型安全性が重要なアプリケーション
- **学習リソース**: [PydanticAI Documentation](https://ai.pydantic.dev/)

## 🤝 コントリビューション

プルリクエストやIssueの報告を歓迎します！

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを開く

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🙏 謝辞

- Google ADK チーム
- LangChain コミュニティ  
- PydanticAI チーム
- 全てのコントリビューター

---

**🤖 このプロジェクトは [Claude Code](https://claude.ai/code) によって生成されました**
EOF < /dev/null