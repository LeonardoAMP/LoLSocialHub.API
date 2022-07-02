from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import db_connection
from repositories import SummonerRepo, SettingRepo
import requests

r = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
SQLALCHEMY_DATABASE_URL = db_connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()
try:
    datadragon_ver = SettingRepo.fetch_by_name(db,name='datadragon_ver')
    datadragon_ver.value = r.json()[0]
    db.commit()
    SummonerRepo.update_summoners_rank(db)
finally:
    db.close()