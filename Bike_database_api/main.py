from typing import Annotated

from fastapi import FastAPI,HTTPException,Depends
from sqlmodel import SQLModel,create_engine,Field,Session

class Bike(SQLModel,table=True):
    id:int|None=Field(default=None,primary_key=True)
    comp_name:str
    full_name:str
    model_no:int
    higest_speed_kmph:float
    price:float

SQLModel_name="Bike_database_api/bike_database.db"
sqlite_url=f"sqlite:///{SQLModel_name}"

connect_args={"check_same_thread":False}
engine=create_engine(sqlite_url,connect_args=connect_args)

def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

Session_Dep=Annotated[Session,Depends(get_session)]    

app=FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_table()

@app.post("/Bike/")
def Bikes(bike:Bike,session:Session_Dep)->Bike:
    session.add(bike)
    session.commit()
    session.refresh(bike) 
    return bike

@app.get("/Bikes/{id}")
def bike_info(id:int,session:Session_Dep)->Bike:
    bikes=session.get(Bike,id)
    if not bikes:
        raise HTTPException(status_code=404,detail="Bike not found") 
    return bikes

@app.delete("/Bikes/{id}")
def delete_bike(id:int,session:Session_Dep):
    bikes=session.get(Bike,id)
    if not bikes:
        raise HTTPException(status_code=404,detail="Bike not found")
    session.delete(bikes)
    session.commit() 
    return {"ok":True}