from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Payment(Base):
	__tablename__ = "payments"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	order_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("orders.id", ondelete="CASCADE"),
		nullable=False,
	)
	provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
	status: Mapped[str | None] = mapped_column(String(50), nullable=True)
	amount: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
	created_at: Mapped[datetime | None] = mapped_column(
		DateTime,
		server_default=text("CURRENT_TIMESTAMP"),
		nullable=True,
	)