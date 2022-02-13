from fastapi import FastAPI, HTTPException
from typing import Optional
import pony.orm as pony
from pony.orm.serialization import to_dict
from pydantic import BaseModel, validator
from models import Satelite, db
from geopy.distance import geodesic 

app = FastAPI()

class SpaceTrackOut(BaseModel): 
    CCSDS_OMM_VERS : str
    COMMENT : str
    CREATION_DATE : Optional[str] 
    ORIGINATOR : str
    OBJECT_NAME : Optional[str]
    OBJECT_ID : Optional[str]
    CENTER_NAME : str
    REF_FRAME : str
    TIME_SYSTEM : str
    MEAN_ELEMENT_THEORY :  str
    EPOCH : Optional[str]
    MEAN_MOTION : Optional[float]
    ECCENTRICITY : Optional[float]
    INCLINATION : Optional[float]
    RA_OF_ASC_NODE : Optional[float]
    ARG_OF_PERICENTER : Optional[float]
    MEAN_ANOMALY : Optional[float]
    EPHEMERIS_TYPE : Optional[int]
    CLASSIFICATION_TYPE : Optional[str]
    NORAD_CAT_ID : int
    ELEMENT_SET_NO : Optional[int]
    REV_AT_EPOCH : Optional[int]
    BSTAR : Optional[float]
    MEAN_MOTION_DOT : Optional[float]
    MEAN_MOTION_DDOT : Optional[float] 
    SEMIMAJOR_AXIS : Optional[float]
    PERIOD : Optional[float]
    APOAPSIS : Optional[float]
    PERIAPSIS : Optional[float]
    OBJECT_TYPE : Optional[str]
    RCS_SIZE : Optional[str]
    COUNTRY_CODE : Optional[str]
    LAUNCH_DATE : Optional[str] 
    SITE : Optional[str]
    DECAY_DATE : Optional[str] 
    DECAYED : Optional[int]
    FILE : Optional[int]
    GP_ID : int
    TLE_LINE0 : Optional[str]
    TLE_LINE1 : Optional[str]
    TLE_LINE2 : Optional[str]
    
    class Config: 
	    orm_mode=True

class SateliteInDB(BaseModel): 
    spaceTrack:  SpaceTrackOut
    launch :  Optional[str]
    version:  Optional[str]
    height_km:  Optional[float]
    latitude:  Optional[float]
    longitude:  Optional[float]
    velocity_kms:  Optional[float]
    id:  str
    @validator('spaceTrack', pre=True, allow_reuse=True)
    def pony_set_to_list(cls, value): 
        value = to_dict(value)["SpaceTrack"]
        value = value[(list(value.keys())[0])]  
        return value
    class Config: 
        orm_mode = True 
        arbitrary_types_allowed = True

#Show information about all satelites
@app.get("/v4/starlink")
async def show_satelites(): 
    with pony.db_session: 
        satelites = Satelite.select()
        result = [SateliteInDB.from_orm(s) for s in satelites]
        return result

#Show information about satelite named {object_name}
@app.get("/v4/starlink/{object_name}")
async def search_by_name(object_name: str):
    with pony.db_session:
        satelites = db.Satelite.select(
            lambda p: p.spaceTrack.OBJECT_NAME == object_name
        )
        result = [SateliteInDB.from_orm(s) for s in satelites]
        if result == []:
            raise HTTPException(
                status_code=404, detail="Not found"
            ) 
        return result

#Show information about satelites within a maximum distance "distance" from (latitude, longitude)
@app.get("/v4/distance/{latitude}+{longitude}+{distance}")
async def search_by_distance(latitude: float, longitude: float, distance: float):
    with pony.db_session:
        if abs(longitude) > 90 or abs(latitude) > 90:
            raise HTTPException(
                status_code=500, detail="Invalid parameters"
            ) 
        satelites = db.Satelite.select(
            lambda p:  p.latitude != None and  p.longitude!= None
        )
        satelites = filter(lambda p: geodesic((p.latitude, p.longitude), (latitude,longitude) ).km <= distance, satelites)
        result = [SateliteInDB.from_orm(s) for s in satelites]
        return result
