from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class Service(Base):
	__tablename__ = "services"

	id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
	title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
	slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
	description: Mapped[str] = mapped_column(Text, nullable=False)
	icon: Mapped[str] = mapped_column(String(255), nullable=False)
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
	price: Mapped[str | None] = mapped_column(String(100), nullable=True)
	short_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
	features: Mapped[dict | list | None] = mapped_column(JSONB, nullable=True)


service_model = Service.__table__
