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
 - 次に、経度緯度をOpenWeatherMapに渡して、天気を得ます
 - 天気をコマンドラインに日本語で出力して終了します


## Commands
- Install dependencies: `uv sync`
- Add dependency: `uv add <package>`
- Run Python: `uv run python`
- Run script: `uv run <script.py>`
- Test: (to be determined)
- Build: (to be determined)
- Lint: (to be determined)

## Notes
- Repository was recently cloned and appears to be empty
- Working directory: /Users/dandaso/claude_home/agentic_workflow_examples
