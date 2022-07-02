from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from db import Base

class Role(Base):
    __tablename__ = 'Roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False)
    order = Column(Integer, nullable=False)
    summoners = relationship("Summoner", back_populates="role")

    def __repr__(self):
        return 'Role(name=%s)' % self.name

class League(Base):
    __tablename__ = 'Leagues'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    order = Column(Integer, nullable=False)
    summoners = relationship("Summoner", back_populates="league")

    def __repr__(self):
        return 'League(name=%s)' % self.name

class Division(Base):
    __tablename__ = 'Divisions'
    id = Column(Integer, primary_key=True)
    name = Column(String(3), nullable=False)
    order = Column(Integer, nullable=False)
    summoners = relationship("Summoner", back_populates="division")

    def __repr__(self):
        return 'Division(name=%s)' % self.name

class Summoner(Base):
    __tablename__ = 'Summoners'
    id = Column(Integer, primary_key=True)
    rank= Column(Integer)
    summoner_name = Column(String(16), nullable=False)
    summoner_icon = Column(String(20), nullable=False)
    riot_id = Column(String(63), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    level = Column(Integer, nullable=False)
    lp = Column(Integer, nullable=False)
    division_id = Column(Integer,ForeignKey('Divisions.id'),nullable=False)
    division =  relationship('Division', back_populates='summoners')
    league_id = Column(Integer,ForeignKey('Leagues.id'), nullable=False)
    league = relationship('League', back_populates='summoners')
    role_id = Column(Integer,ForeignKey('Roles.id'), nullable=False)
    role = relationship('Role', back_populates='summoners')

    def __repr__(self):
        return 'Summoner(summoner_name=%s)' % self.summoner_name

class Setting(Base):
    __tablename__ = 'Settings'
    name = Column(String, primary_key=True)
    value = Column(String, nullable=False)