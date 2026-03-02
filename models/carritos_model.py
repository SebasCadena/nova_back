from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Cart(Base):
	__tablename__ = "cart"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	user_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("users.id", ondelete="CASCADE"),
		nullable=False,
		unique=True,
	)
	created_at: Mapped[datetime | None] = mapped_column(
		DateTime,
		server_default=text("CURRENT_TIMESTAMP"),
		nullable=True,
	)
	updated_at: Mapped[datetime | None] = mapped_column(
		DateTime,
		server_default=text("CURRENT_TIMESTAMP"),
		nullable=True,
	)


carrito_model = Cart.__table__