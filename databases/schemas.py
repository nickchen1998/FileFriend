from sqlalchemy import Column, ForeignKey, Integer, String, Table, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

# 創建關聯表
file_tag_association = Table(
    'file_tag_association',
    Base.metadata,
    Column('file_id', Integer, ForeignKey('file.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    size = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    hashcode = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tags = relationship('Tag', secondary=file_tag_association, back_populates='files')


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    files = relationship('File', secondary=file_tag_association, back_populates='tags')
