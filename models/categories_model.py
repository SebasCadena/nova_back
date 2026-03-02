from datetime import datetime

from sqlalchemy import DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Category(Base):
	__tablename__ = "categories"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
	slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=text("CURRENT_TIMESTAMP"),
		nullable=False,
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=text("CURRENT_TIMESTAMP"),
		nullable=False,
	)


category_model = Category.__table__
