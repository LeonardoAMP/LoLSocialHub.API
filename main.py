from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from db import get_db, engine
import models as models
import schemas as schemas
from repositories import SettingRepo, SummonerRepo, RoleRepo, DivisionRepo, LeagueRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List

app = FastAPI(title="Lol Social Hub - API",
    description="API for a League of Legends social Hub",
    version="1.0.0",)

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.get('/summoners', tags=["Summoner"],response_model=List[schemas.Summoner])
def get_all_summoners(db: Session = Depends(get_db)):
    """
    Get all the Summoners stored in database
    """
    return SummonerRepo.fetch_all(db)

@app.post('/summoner', tags=["Summoner"],response_model=schemas.Summoner,status_code=201)
async def create_summoner(summoner_request: schemas.SummonerCreate, db: Session = Depends(get_db)):
    """
    Create an Summoner and store it in the database
    """    
    db_summoner = SummonerRepo.fetch_by_name(db, name=summoner_request.summoner_name)
    if db_summoner:
        db_summoner.role_id = summoner_request.role_id
        db.commit()
        return db_summoner
        #raise HTTPException(status_code=400, detail="Summoner already exists!")

    return await SummonerRepo.create(db=db, data=summoner_request)

@app.get('/roles', tags=["Role"],response_model=List[schemas.Role])
def get_all_roles(db: Session = Depends(get_db)):
    """
    Get all the Roles stored in database
    """
    return RoleRepo.fetch_all(db)

@app.get('/divisions', tags=["Division"],response_model=List[schemas.Division])
def get_all_divisions(db: Session = Depends(get_db)):
    """
    Get all the Divisions stored in database
    """
    return DivisionRepo.fetch_all(db)

@app.get('/leagues', tags=["League"],response_model=List[schemas.League])
def get_all_divisions(db: Session = Depends(get_db)):
    """
    Get all the Leagues stored in database
    """
    return LeagueRepo.fetch_all(db)

@app.get('/settings', tags=["Setting"],response_model=List[schemas.Setting])
def get_setting_by_name(name: str,db: Session = Depends(get_db)):
    """
    Get a setting by its name stored in database
    """    
    setting = SettingRepo.fetch_by_name(db,name)
    return setting

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)