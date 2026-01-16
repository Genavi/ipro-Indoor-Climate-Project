from sqlalchemy import Column, Integer, Text, ForeignKey, Float, Numeric, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Distributor(Base):
    __tablename__ = "distributors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    website = Column(Text)

    readers = relationship("Reader", back_populates="distributor_rel")
    components = relationship("Component", back_populates="distributor_rel")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    readings = relationship("SensorReading", back_populates="location_rel")

class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    distributor = Column(Integer, ForeignKey("distributors.id"))

    distributor_rel = relationship("Distributor", back_populates="readers")
    components = relationship("Component", back_populates="reader_rel")
    readings = relationship("SensorReading", back_populates="reader_rel")

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    reader = Column(Integer, ForeignKey("readers.id"))
    distributor = Column(Integer, ForeignKey("distributors.id"))
    price_per_unit = Column(Numeric(10, 2))
    website = Column(Text)

    distributor_rel = relationship("Distributor", back_populates="components")
    reader_rel = relationship("Reader", back_populates="components")

class SensorReading(Base):
    __tablename__ = "sensor_readings"

    timestamp = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    reader = Column(Integer, ForeignKey("readers.id"))
    location = Column(Integer, ForeignKey("locations.id"))
    sensor_0_name = Column(Text)
    sensor_0_value = Column(Float)
    sensor_1_name = Column(Text)
    sensor_1_value = Column(Float)
    sensor_2_name = Column(Text)
    sensor_2_value = Column(Float)
    sensor_3_name = Column(Text)
    sensor_3_value = Column(Float)
    sensor_4_name = Column(Text)
    sensor_4_value = Column(Float)

    reader_rel = relationship("Reader", back_populates="readings")
    location_rel = relationship("Location", back_populates="readings")
