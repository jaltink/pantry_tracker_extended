# pantry_tracker/webapp/models.py - UITGEBREIDE VERSIE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()

class Location(Base):
    """Opslaglocaties: vriezer, kelder, voorraadkast, etc. - NIEUW"""
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    
    products = relationship("Product", back_populates="location")

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    barcode = Column(String, unique=True, nullable=True)
    image_front_small_url = Column(String, nullable=True)
    
    # NIEUWE VELDEN
    min_stock = Column(Integer, nullable=False, default=5)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    expiry_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    
    category = relationship("Category", back_populates="products")
    location = relationship("Location", back_populates="products")
    count = relationship("Count", back_populates="product", uselist=False, cascade="all, delete-orphan")
    
    def is_low_stock(self):
        """Check of voorraad laag is"""
        if self.count:
            return self.count.count <= self.min_stock
        return False
    
    def days_until_expiry(self):
        """Dagen tot vervaldatum"""
        if not self.expiry_date:
            return None
        return (self.expiry_date - date.today()).days
    
    def is_expired(self):
        """Is product verlopen"""
        days = self.days_until_expiry()
        return days is not None and days < 0
    
    def is_expiring_soon(self, threshold=7):
        """Verloopt binnenkort (binnen X dagen)"""
        days = self.days_until_expiry()
        return days is not None and 0 <= days <= threshold

class Count(Base):
    __tablename__ = 'counts'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), unique=True, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    
    product = relationship("Product", back_populates="count")
