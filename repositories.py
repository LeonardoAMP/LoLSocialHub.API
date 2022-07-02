from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from riotwatcher import LolWatcher
from datetime import datetime
from pytz import timezone
import os
import time

W = LolWatcher(os.environ['RIOT_API_KEY'])
REGION = os.environ['LOLWATCHER_REGIN']

class SummonerRepo:
    def fetch_by_name(db: Session,name):
        return db.query(models.Summoner).filter(func.lower(models.Summoner.summoner_name) == name.lower()).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        results = db.query(models.Summoner).offset(skip).limit(limit).order_by(models.Summoner.rank).all()        
        #results = db.query(models.Summoner).options(joinedload('division'), joinedload('role'),joinedload('league')).offset(skip).limit(limit).all()
        return results    

    async def create(db: Session, data: schemas.SummonerCreate):
        try:
            summoner = W.summoner.by_name(REGION, data.summoner_name)

        except Exception as e:
            #TODO: Log Error
            return {'message': 'Summoner name not found.'}, 500

        new_summoner = models.Summoner()
        new_summoner.creation_date = datetime.now().astimezone(
            timezone('America/Santo_Domingo'))
        new_summoner.role_id = data.role_id
        new_summoner.summoner_name = summoner['name']
        new_summoner.summoner_icon = summoner['profileIconId']
        new_summoner.riot_id = summoner['id']
        new_summoner.level = summoner['summonerLevel']
        SummonerRepo.update_rank_entry(db, new_summoner)
        db.add(new_summoner)
        db.commit()
        SummonerRepo.update_rank_index(db)
        db.refresh(new_summoner)
        return new_summoner

    def update_summoners_rank(db: Session):
        """Actualiza la info de los summoners y su ID."""
        summoners = SummonerRepo.fetch_all(db)
        now = datetime.now()
        valor_tiempo = SettingRepo.fetch_by_name(db, 'last_rank_update')
        if not valor_tiempo:            
            valor_tiempo = models.Setting(name='last_rank_update', value=now.strftime('%Y-%m-%d %H:%M:%S.%f'))
            valor_tiempo.save()

        last_execution = datetime.strptime(valor_tiempo.Valor, '%Y-%m-%d %H:%M:%S.%f')

        if (now - last_execution).total_seconds() < 300:
            return #HttpResponse(json.dumps({'rs':'La actualización fue disparada por otro usuario recientemente. Vuelva a intentar dentro de '+ str((tiempo - tiempo2).total_seconds())+' segundos.'}))


        for summoner in summoners:
            riot_summoner = W.summoner.by_name(REGION, summoner.Nombre)
            summoner.SummonerIcon = riot_summoner['profileIconId']
            summoner.Id = riot_summoner['id']
            summoner.Nombre = riot_summoner['name']
            summoner.Lv = riot_summoner['summonerLevel']
            SummonerRepo.update_rank_entry(db, summoner)
            time.sleep(5)
        
        db.commit()
        SummonerRepo.update_rank_index(db)        
        valor_tiempo.Valor = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        db.commit()
    
    def update_rank_entry(db: Session, summoner: models.Summoner):
        rank_entries = W.league.by_summoner(REGION, summoner.riot_id)
        solo_rank_entry = None

        for rank_entry in rank_entries:
            if rank_entry['queueType'] == 'RANKED_SOLO_5x5':
                solo_rank_entry = rank_entry

        if solo_rank_entry != None:
            league_id =  db.query(models.League).filter(models.League.name == solo_rank_entry['tier']).first().id
            summoner.league_id = league_id

            division_id = db.query(models.Division).filter(models.Division.name == solo_rank_entry['rank']).first().id
            summoner.division_id = division_id
            summoner.lp = solo_rank_entry['leaguePoints']            
            summoner.rank = 0
        else:
            summoner.league_id = 1
            summoner.division_id = 1
            summoner.lp = '0'
            summoner.rank = 0
    
    def update_rank_index(db: Session):
        summoners = db.query(models.Summoner).join(models.Summoner.league).join(models.Summoner.division).order_by(
            models.League.order.desc(),
            models.Division.order.desc(),
            models.Summoner.lp.desc(),
            models.Summoner.level.desc()).all()
        
        rank = 1
        for summoner in summoners:
            summoner.rank = rank
            rank+=1
        db.commit()

class RoleRepo:
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        results = db.query(models.Role).offset(skip).limit(limit).all()
        return results

class DivisionRepo:
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        results = db.query(models.Division).offset(skip).limit(limit).all()
        return results

class LeagueRepo:
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        results = db.query(models.League).offset(skip).limit(limit).all()
        return results

class SettingRepo:
    def fetch_by_name(db: Session, name):
        return db.query(models.Setting).filter(func.lower(models.Setting.name) == name.lower()).first()
