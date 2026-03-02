from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Order(Base):
	__tablename__ = "orders"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	user_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
	)
	status: Mapped[str | None] = mapped_column(String(50), server_default=text("'pending'"), nullable=True)
	total: Mapped[Decimal] = mapped_column(Numeric(10, 2), server_default=text("0.00"), nullable=False)
	created_at: Mapped[datetime | None] = mapped_column(
		DateTime,
		server_default=text("CURRENT_TIMESTAMP"),
		nullable=True,
	)


order_model = Order.__table__