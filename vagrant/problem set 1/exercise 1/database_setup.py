#!/usr/bin/python

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Shelter(Base):
    __tablename__ = 'shelter'

    name = Column(String(250), nullable=False)
    address = Column(String(250))
    city = Column(String(250))
    state = Column(String(250))
    zipCode = Column(String(250))
    website = Column(String(250))
    id = Column(Integer, primary_key=True)
    


class Puppy(Base):
    __tablename__ = 'puppy'

    name = Column(String(80), primary_key=True)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(7), nullable=False)
    weight = Column(Float)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


engine = create_engine('sqlite:///puppies.db')


Base.metadata.create_all(engine)

