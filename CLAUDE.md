# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がこのリポジトリで作業する際のガイダンスを提供します。

## プロジェクト概要

[unoserver](https://github.com/unoconv/unoserver)（LibreOfficeベースのドキュメント変換サーバー）をDockerで利用するサンプルプロジェクト。Dockerイメージは `fufuhu/unoserver` を使用。主要言語はPython。

## 開発コマンド

- サーバー起動: `docker compose up`
- バックグラウンド起動: `docker compose up -d`
- 停止: `docker compose down`

## アーキテクチャ

- unoserverはポート2003で公開（`docker-compose.yml`で定義）
