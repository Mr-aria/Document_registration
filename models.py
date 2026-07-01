import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///camelot.db")
engine = create_engine(DATABASE_URL)
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pytz

Base = declarative_base()
engine = create_engine('sqlite:///camelot.db', echo=False)
Session = sessionmaker(bind=engine)

# منطقه زمانی تهران
TEHRAN_TZ = pytz.timezone('Asia/Tehran')

def now_tehran():
    return datetime.now(TEHRAN_TZ)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # telegram user id
    username = Column(String, nullable=True)
    camelot_name = Column(String, nullable=False)
    national_code = Column(String, nullable=False)
    bank_account = Column(String, nullable=False)
    registered_at = Column(DateTime, default=now_tehran)
    is_blacklisted = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, nullable=False)  # telegram id فروشنده
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    post_link = Column(String, nullable=False)
    unique_code = Column(String(8), unique=True, nullable=False)
    created_at = Column(DateTime, default=now_tehran)
    is_sold = Column(Boolean, default=False)
    buyer_id = Column(Integer, nullable=True)  # when sold

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    product_code = Column(String(8), nullable=False)
    buyer_id = Column(Integer, nullable=False)
    seller_id = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    bank_transaction_code = Column(String(12), unique=True, nullable=False)
    status = Column(String, default='pending')  # pending, confirmed, failed
    created_at = Column(DateTime, default=now_tehran)
    confirmed_at = Column(DateTime, nullable=True)
    forwarded_message_text = Column(Text, nullable=True)  # برای لاگ

class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=now_tehran)

class BotConfig(Base):
    __tablename__ = 'bot_config'
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)

# ایجاد جداول
Base.metadata.create_all(engine)