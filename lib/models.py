from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Float, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

dev_companies = Table('dev_companies', Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('dev_id', Integer, ForeignKey('devs.id')),
    extend_existing=True
)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    devs = relationship('Dev', secondary=dev_companies, back_populates='companies')
    freebies = relationship('Freebie', backref=backref('companies'))
    

    def __repr__(self):
        return f'<Company {self.name}>'
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Float())

    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    companies = relationship('Company', secondary=dev_companies, back_populates='devs')
    freebies = relationship('Freebie', backref=backref('devs'))


    def __repr__(self):
        return f'<Dev {self.name}>'
