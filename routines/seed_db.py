from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models as models
from models import *
import os

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
SQLALCHEMY_DATABASE_URL = uri
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

league1 = League(
    id =1,
    name='PROVISIONAL',
    order= 1
)
league2 = League(
    id =2,
    name= 'IRON',
    order= 2
)
league3 = League(
    id =3,
    name= 'SILVER',
    order= 3
)
league4 = League(
    id =4,
    name= 'GOLD',
    order= 4
)
league5 = League(
    id =5,
    name= 'PLATINUM',
    order= 5
)
league6 = League(
    id =6,
    name= 'DIAMOND',
    order= 6
)
league7 = League(
    id =7,
    name= 'MASTER',
    order= 7
)
league8 = League(
    id =8,
    name= 'GRANDMASTER',
    order= 8
)
league9 = League(
    id =9,
    name='CHALLENGER',
    order=9
)
db.add(league1)
db.add(league2)
db.add(league3)
db.add(league4)
db.add(league5)
db.add(league6)
db.add(league7)
db.add(league8)
db.add(league9)
db.commit()

role1 = Role(
    id =1,
    name='Top',
    order=1
)
role2 = Role(
    id =2,
    name='Jungle',
    order=2
)
role3 = Role(
    id =3,
    name='Mid',
    order=3
)
role4 = Role(
    id =4,
    name='Adc',
    order=4
)
role5 = Role(
    id =5,
    name='Support',
    order=5
)
db.add(role1)
db.add(role2)
db.add(role3)
db.add(role4)
db.add(role5)
db.commit()

division1 = Division(
    id =1,
    name='I',
    order=1
)
division2 = Division(
    id =2,
    name='II',
    order=2
)
division3 = Division(
    id =3,
    name='III',
    order=3
)
division4 = Division(
    id =4,
    name='IV',
    order=4
)

db.add(division1)
db.add(division2)
db.add(division3)
db.add(division4)
db.commit()

setting1 = Setting(
    name='datadragon_ver',
    value='12.12.1'
)
db.add(setting1)
db.commit()
db.close()