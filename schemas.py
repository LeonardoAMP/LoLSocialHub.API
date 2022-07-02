from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class Division(BaseModel):
    id: int
    name: str
    order: int

    class Config:
        orm_mode = True

class League(BaseModel):
    id: int
    name: str
    order: int

    class Config:
        orm_mode = True

class Role(BaseModel):
    id: int
    name: str
    order: int

    class Config:
        orm_mode = True


class Setting(BaseModel):
    name: str
    value: str

    class Config:
        orm_mode = True

class SummonerBase(BaseModel):
    summoner_name: str
    role_id: int

class SummonerCreate(SummonerBase):    
    pass

class Summoner(SummonerBase):
    id: int
    rank: int
    summoner_name: str
    summoner_icon: str
    riot_id: str
    creation_date: datetime
    level: int
    lp: int
    division_id: int
    role_id: int
    role: Role
    division: Division
    league: League

    class Config:
        orm_mode = True
