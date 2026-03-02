from decimal import Decimal

from sqlalchemy import BigInteger, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class OrderItem(Base):
	__tablename__ = "order_items"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	order_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("orders.id", ondelete="CASCADE"),
		nullable=False,
	)
	product_id: Mapped[int] = mapped_column(
		BigInteger,
		ForeignKey("products.id", ondelete="CASCADE"),
		nullable=False,
	)
	quantity: Mapped[int] = mapped_column(Integer, nullable=False)
	price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)


order_items_model = OrderItem.__table__