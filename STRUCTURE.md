# プロジェクト構成（ICTrenshu）

更新日: 2025-10-02

## ルート直下
- `.env` — docker-compose 等で参照する環境変数（開発用）
- `.git/` — Git リポジトリメタデータ
- `.gitignore` — Git で無視するファイル定義
- `alembic/` — DB マイグレーション用フォルダ
- `alembic.ini` — Alembic 設定ファイル（テンプレ）
- `api/` — バックエンド API（FastAPI）関連
- `docker-compose.yml` — API/DB を起動する Compose 定義（テンプレ）
- `README.md` — プロジェクト説明
- `scripts/` — ユーティリティスクリプト置き場（現状空）
- `tests/` — テストコード置き場（現状空）

---

## alembic/
- `env.py` — Alembic 実行時のエントリポイント
- `versions/` — マイグレーションファイルの保存先（現状空）

---

## api/
- `Dockerfile` — API サービスのビルド用 Dockerfile（テンプレ）
- `requirements.txt` — API 依存パッケージ（テンプレ）
- `app/` — アプリケーション本体

### api/app/
- `__init__.py` — パッケージ化用の空ファイル
- `main.py` — FastAPI エントリポイント（テンプレ）
- `db.py` — DB 接続（SQLAlchemy）定義（テンプレ）
- `models.py` — ORM モデル定義（テンプレ）
- `routers/` — 旧来のルーター置き場（MVP 簡易版）
- `api/` — 公式なバージョニング配下（/api/v1）
- `schemas/` — Pydantic スキーマ（現状空）
- `services/` — ドメインロジック層（現状空）
- `repositories/` — リポジトリ層（現状空）
- `core/` — 設定/共通処理（現状空）
- `db/` — DB 関連（初期化/Session 等の将来用）

#### api/app/routers/
- `__init__.py` — パッケージ化用
- `reports.py` — 日報 API の簡易ルーター（テンプレ）

#### api/app/api/v1/
- `__init__.py` — パッケージ化用
- `endpoints/` — バージョン付きエンドポイント置き場

##### api/app/api/v1/endpoints/
- `__init__.py` — パッケージ化用（現状空）

#### api/app/schemas/
- `__init__.py` — パッケージ化用（現状空）

#### api/app/services/
- `__init__.py` — パッケージ化用（現状空）

#### api/app/repositories/
- `__init__.py` — パッケージ化用（現状空）

#### api/app/core/
- `__init__.py` — パッケージ化用（現状空）

#### api/app/db/
- `__init__.py` — パッケージ化用（現状空）

---

## scripts/
- （現状空）

## tests/
- `__init__.py` — パッケージ化用（現状空）

---

備考:
- いまは雛形のため中身は最小限/空が多いです。今後 API 実装、マイグレーション、テストを段階的に追加していきます。
