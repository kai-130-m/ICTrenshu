import argparse
import csv
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime, time, date

from sqlalchemy.dialects.postgresql import insert as pg_insert  # kept for potential future use
from sqlalchemy import text

from .db import SessionLocal, Base, engine
from .models import DailyReport


def detect_encoding(path: Path) -> str:
    # UTF-8(BOM) → UTF-8 → CP932 の優先順で判定
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    try:
        raw.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        return "cp932"


def parse_date(value: Optional[str]) -> Optional[date]:
    s = (value or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y年%m月%d日"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_time(value: Optional[str]) -> Optional[time]:
    s = (value or "").strip()
    if not s:
        return None
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(s, fmt).time()
        except ValueError:
            continue
    # 小数時間は非対応
    raise ValueError(f"invalid time: {value}")


def parse_minutes(value: Optional[str]) -> Optional[int]:
    s = (value or "").strip()
    if not s:
        return None
    s = s.replace("分", "")
    if ":" in s:
        try:
            h, m = s.split(":", 1)
            return int(h) * 60 + int(m)
        except Exception:
            return None
    # 小数は非対応。整数のみ
    return int(s)


def row_get(row: dict, *keys: str) -> Optional[str]:
    for k in keys:
        if k in row:
            v = row.get(k)
            if v is not None and str(v).strip() != "":
                return str(v)
    return None


def import_csv(csv_path: Path) -> Tuple[int, int]:
    # 念のためテーブルを作成（API起動前に実行してもOK）
    Base.metadata.create_all(bind=engine)

    enc = detect_encoding(csv_path)
    inserted = 0
    skipped = 0

    with csv_path.open("r", encoding=enc, newline="") as f:
        reader = csv.DictReader(f)
        with SessionLocal() as db:
            for row in reader:
                try:
                    data = {
                        # 日付列: "日付" or "報告日" を許容
                        "report_date": parse_date(row_get(row, "日付", "報告日")),
                        # 社員列
                        "employee": (row_get(row, "社員", "氏名") or "").strip() or None,
                        # 時刻
                        "start_at": parse_time(row_get(row, "開始", "開始時刻")),
                        "end_at": parse_time(row_get(row, "終了", "終了時刻")),
                        # 分
                        "overtime_minutes": parse_minutes(row_get(row, "残業")),
                        "midnight_minutes": parse_minutes(row_get(row, "深夜")),
                        # 作業スロット
                        "in_time": parse_time(row_get(row, "入時間", "開始時間")),
                        "out_time": parse_time(row_get(row, "終了時間", "退勤時間")),
                        "elapsed_minutes": parse_minutes(row_get(row, "経過時間")),
                        # テキスト
                        "destination": row_get(row, "行先", "行き先"),
                        "work_content": row_get(row, "作業内容", "業務内容"),
                        "companion": row_get(row, "同行者"),
                    }

                    # 必須チェック
                    if not data["report_date"] or not data["employee"]:
                        skipped += 1
                        continue

                    # 常にINSERT（重複も許容）
                    db.add(DailyReport(**data))
                    db.commit()
                    inserted += 1
                except Exception:
                    db.rollback()
                    skipped += 1

    return inserted, skipped


def main():
    parser = argparse.ArgumentParser(description="Import daily reports CSV into DB")
    parser.add_argument("--file", required=True, help="CSV file path inside container (e.g. /data/csv/xxx.csv)")
    parser.add_argument("--truncate", action="store_true", help="取り込み前にテーブルを空にする（IDもリセット）")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"CSV not found: {path}")
        raise SystemExit(1)

    # テーブルを用意
    Base.metadata.create_all(bind=engine)

    if args.truncate:
        with SessionLocal() as db:
            db.execute(text("TRUNCATE daily_reports RESTART IDENTITY"))
            db.commit()
            print("[daily_reports] truncated (restart identity)")

    ins, skip = import_csv(path)
    print(f"Imported: inserted={ins}, skipped={skip}")


if __name__ == "__main__":
    main()
