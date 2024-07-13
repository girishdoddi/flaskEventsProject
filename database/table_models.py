from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, Boolean

from database.connect_database import Base, engine

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, autoincrement=True)
    name = Column(String(32))
    email = Column(String(32), unique= True)
    password = Column(String(100))
    createdat = Column(DateTime)
    is_verified = Column(Boolean)

class OTP(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    otp = Column(Integer)
    created_at = Column(DateTime)


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String(100))
    price_per_product = Column(Integer)
    quantity = Column(Integer)
    created_at = Column(DateTime)

class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key= True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_name = Column(String(100))
    quantity = Column(Integer)
    total_price = Column(Integer)
    created_at = Column(DateTime)


Base.metadata.create_all(engine)

