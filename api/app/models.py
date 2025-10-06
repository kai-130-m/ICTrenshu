from sqlalchemy import (
	Column,
	BigInteger,
	Text,
	Date,
	Time,
	Integer,
	TIMESTAMP,
	Index,
	text,
)
from .db import Base


class DailyReport(Base):
	__tablename__ = "daily_reports"

	id = Column(BigInteger, primary_key=True, autoincrement=True)

	# 基本情報
	report_date = Column(Date, nullable=False)           # 報告日
	employee = Column(Text, nullable=False)              # 社員

	# 時刻・時間（例の1行に合わせたフィールド）
	start_at = Column(Time(timezone=False), nullable=True)       # 開始（例: 8:15）
	end_at = Column(Time(timezone=False), nullable=True)         # 終了（例: 18:30）

	overtime_minutes = Column(Integer, nullable=True)            # 残業（分）例: 15
	midnight_minutes = Column(Integer, nullable=True)            # 深夜（分）例: 0

	in_time = Column(Time(timezone=False), nullable=True)        # 入時間（例: 8:15）
	out_time = Column(Time(timezone=False), nullable=True)       # 終了時間（例: 8:45）
	elapsed_minutes = Column(Integer, nullable=True)             # 経過時間（分）例: 30

	destination = Column(Text, nullable=True)                    # 行先
	work_content = Column(Text, nullable=True)                   # 作業内容
	companion = Column(Text, nullable=True)                      # 同行者（NULL可）

	created_at = Column(
		TIMESTAMP(timezone=True), nullable=False, server_default=text("timezone('utc', now())")
	)
	updated_at = Column(
		TIMESTAMP(timezone=True),
		nullable=False,
		server_default=text("timezone('utc', now())"),
		server_onupdate=text("timezone('utc', now())"),
	)

	__table_args__ = (
		Index("idx_daily_reports_date", "report_date"),
		Index("idx_daily_reports_employee_date", "employee", "report_date"),
	)
 
