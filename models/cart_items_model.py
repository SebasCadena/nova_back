from sqlalchemy import BigInteger, ForeignKey, Integer, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base_model import Base


class CartItem(Base):
	__tablename__ = "cart_items"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
	cart_id: Mapped[int] = mapped_column(
		Integer,
		ForeignKey("cart.id", ondelete="CASCADE"),
		nullable=False,
	)
	product_id: Mapped[int] = mapped_column(
		BigInteger,
		ForeignKey("products.id", ondelete="CASCADE"),
		nullable=False,
	)
	quantity: Mapped[int] = mapped_column(Integer, server_default=text("1"), nullable=False)


cart_items_model = CartItem.__table__