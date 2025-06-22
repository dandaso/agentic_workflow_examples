# CLAUDE.md

これはClaudeCodeこのプロジェクトで常に参照するClaude codeのメモリファイルです

## Project Overview

このプロジェクトは、Pythonで3個のライブラリを使ったAgenticWorkflowのPythonのサンプルです。
プロジェクトはuvを使って管理します。

ディレクトリ構成は以下の通りです
```
agentic_workflow_examples
 |- adk (GoogleADKを使ったワークフローのサンプル)
 |- pydanticai (PydanticAIを使ったワークフローのサンプル)
 `- langchain (LangChainを使ったワークフローのサンプル)
```

## サンプルアプリの内容
サンプルアプリはコマンドラインアプリで、下記を行います
 - まずコンソールの入力として、天気を知りたい都市名を求めてきます
 - 都市名を入力すると、Google Maps Geocoding APIから経度緯度に変換します
 - 次に、経度緯度をGoogle Weather APIに渡して、天気を得ます
 - 天気をコマンドラインに日本語で出力して終了します
 - サンプルなので、いったんテストはいらないです


## Commands
- Install dependencies: `uv sync`
- Add dependency: `uv add <package>`
- Run Python: `uv run python`
- Run script: `uv run <script.py>`
- Test: (to be determined)
- Build: (to be determined)
- Lint: (to be determined)

## 実装ステータス

### PydanticAI (完了)
- ✅ 基本セットアップ
- ✅ Google Maps Geocoding API統合
- ✅ Google Weather API統合
- ✅ エラーハンドリングとフォールバック機能

### LangChain (進行中)
- ✅ 基本セットアップ
- ✅ 地理座標取得機能 (get_city_coordinates tool)
- 🚧 天気API呼び出し機能 (get_weather_data tool) - 実装完了、PRペンディング
- ⏳ 統合テストとエラーハンドリング

### Google ADK (未着手)
- ⏳ 基本セットアップ
- ⏳ 地理座標取得機能
- ⏳ 天気API呼び出し機能

## Notes
- 現在はLangChain実装のIssue #18 (天気API呼び出し機能) を作業中
- Google Weather APIを使用（OpenWeatherMapから変更）
- 各ライブラリで共通のWeatherAgentインターフェースを使用
- Working directory: /Users/dandaso/claude_home/agentic_workflow_examples
