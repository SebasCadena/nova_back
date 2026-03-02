from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Product(Base):
	__tablename__ = "products"

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
	slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
	description: Mapped[str] = mapped_column(Text, nullable=False)
	price: Mapped[float | None] = mapped_column(Float, nullable=True)
	image_url: Mapped[str] = mapped_column(String(500), nullable=False)
	category_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("categories.id", onupdate="CASCADE", ondelete="CASCADE"),
		nullable=False,
	)
	is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
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
	stok: Mapped[int | None] = mapped_column(Integer, nullable=True)


product_model = Product.__table__
