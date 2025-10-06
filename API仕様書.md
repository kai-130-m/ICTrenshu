# Daily Reports API 仕様書

このドキュメントは、現在の実装（FastAPI + PostgreSQL）の公開エンドポイントと入出力仕様を示します。テンプレートから本プロジェクトの実体に置き換えています。

## 基本情報

| 項目 | 値 |
| --- | --- |
| ホスト | http://localhost:8000 |
| ベースパス | /v1 |
| データ形式 | application/json; charset=utf-8 |

## ステータスコード

- 200: 成功
- 400: リクエスト不正（型/範囲エラー等）
- 500: サーバ内部エラー

## ヘルスチェック

| メソッド | パス |
| --- | --- |
| GET | /healthz |

レスポンス（200）
```json
{ "status": "ok" }
```

## 日報一覧取得

| メソッド | パス |
| --- | --- |
| GET | /v1/daily-reports |

概要: 直近のreport_date降順で日報を返却します。デフォルト50件。

クエリパラメータ

| 名称 | 型 | 必須 | 既定値 | 説明 |
| --- | --- | --- | --- | --- |
| limit | integer | 任意 | 50 | 取得件数（1-200推奨） |

レスポンス（200）
```json
{
  "items": [
    {
      "id": 1,
      "report_date": "2025-09-01",
      "employee": "社員A",
      "start_at": "08:15:00",
      "end_at": "18:30:00",
      "overtime_minutes": 15,
      "midnight_minutes": 0,
      "in_time": "08:15:00",
      "out_time": "08:45:00",
      "elapsed_minutes": 30,
      "destination": "会社A発寒",
      "work_content": "残確認",
      "companion": null
    }
  ],
  "count": 1
}
```

注意事項
- 文字列のエンコーディングはUTF-8です（CSV取り込み時にUTF-8優先で読込）。
- `id` はサーバ側で自動採番されます。
- データは重複許可です（同一社員×同一日でも複数行あり得ます）。

## データモデル（保存スキーマ）

テーブル名: daily_reports

| カラム | 型 | 必須 | 説明 |
| --- | --- | --- | --- |
| id | bigint | Yes | 主キー（自動採番） |
| report_date | date | Yes | 報告日（JSTの概念日） |
| employee | text | Yes | 社員名 |
| start_at | time | No | 開始時刻（例: 08:15:00） |
| end_at | time | No | 終了時刻（例: 18:30:00） |
| overtime_minutes | integer | No | 残業分 |
| midnight_minutes | integer | No | 深夜分 |
| in_time | time | No | 入時間 |
| out_time | time | No | 終了時間 |
| elapsed_minutes | integer | No | 経過時間（分） |
| destination | text | No | 行先 |
| work_content | text | No | 作業内容 |
| companion | text | No | 同行者 |
| created_at | timestamptz | Yes | 生成時刻（UTC） |
| updated_at | timestamptz | Yes | 更新時刻（UTC） |

インデックス
- idx_daily_reports_date (report_date)
- idx_daily_reports_employee_date (employee, report_date)

## CSV 取り込みの前提

- 取込パス: コンテナ内 `/data/csv/xxx.csv`
- 文字コード: UTF-8(BOM/UTF-8) 優先、失敗時にCP932
- 対応ヘッダー例: 報告日, 社員, 開始, 終了, 残業, 深夜, 入時間, 終了時間, 経過時間, 行先, 作業内容, 同行者
- 時刻: HH:MM または HH:MM:SS のみ（小数時間は非対応）
- 分: "15", "0", "HH:MM", "15分" を許容
- 重複行: 許容（常にINSERT）

実行例
```bash
docker exec -it ictrenshu-api python -m app.import_daily_reports --file /data/csv/dailyrepot_sample01.csv
```

## 今後の拡張（案）
- 一覧APIの検索条件（employee, date_from, date_to）
- ページング（offset/limit）
- 詳細取得・登録/更新API
- 認証・認可、監査ログ
