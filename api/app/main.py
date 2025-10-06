from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from .db import Base, engine, get_db
from .models import DailyReport

app = FastAPI(title="Daily Reports API", version="0.1.0")


@app.on_event("startup")
def on_startup():
	# MVP: 自動でテーブルを作成（本番前に Alembic へ移行予定）
	Base.metadata.create_all(bind=engine)


@app.get("/healthz")
def healthz(db: Session = Depends(get_db)):
	db.execute(text("SELECT 1"))
	return {"status": "ok"}


@app.get("/")
def root():
	return {"message": "Daily Reports API"}


@app.get("/v1/daily-reports")
def list_daily_reports(limit: int = 50, db: Session = Depends(get_db)):
	# シンプルな一覧（直近のreport_date降順）
	q = db.query(DailyReport).order_by(DailyReport.report_date.desc()).limit(limit)
	rows = q.all()
	items = []
	for r in rows:
		items.append(
			{
				"id": r.id,
				"report_date": r.report_date.isoformat() if (r.report_date is not None) else None,
				"employee": r.employee,
				"start_at": r.start_at.isoformat() if (r.start_at is not None) else None,
				"end_at": r.end_at.isoformat() if (r.end_at is not None) else None,
				"overtime_minutes": r.overtime_minutes,
				"midnight_minutes": r.midnight_minutes,
				"in_time": r.in_time.isoformat() if (r.in_time is not None) else None,
				"out_time": r.out_time.isoformat() if (r.out_time is not None) else None,
				"elapsed_minutes": r.elapsed_minutes,
				"destination": r.destination,
				"work_content": r.work_content,
				"companion": r.companion,
			}
		)

	return {"items": items, "count": len(items)}
