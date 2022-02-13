#This file was made for testing purposes only, it matches our database data with https://api.spacexdata.com/v4/starlink

import os
if os.path.exists("database.satelite"):
    os.remove("database.satelite")
import pony.orm as pony
from models import db
import requests

resp = requests.get('https://api.spacexdata.com/v4/starlink')
satelites = resp.json()

for satelite in satelites:
    if satelite["spaceTrack"]["DECAY_DATE"] == None:
        satelite["spaceTrack"]["DECAY_DATE"] = "null"
    if satelite["spaceTrack"]["RCS_SIZE"] == None:
        satelite["spaceTrack"]["RCS_SIZE"] = "null"
    if satelite["spaceTrack"]["COUNTRY_CODE"] == None:
        satelite["spaceTrack"]["COUNTRY_CODE"] = "null"
    if satelite["spaceTrack"]["LAUNCH_DATE"] == None:
        satelite["spaceTrack"]["LAUNCH_DATE"] = "null"
    if satelite["spaceTrack"]["SITE"] == None:
        satelite["spaceTrack"]["SITE"] = "null"
    with pony.db_session:
        st1 = db.SpaceTrack(
            CCSDS_OMM_VERS = satelite["spaceTrack"]["CCSDS_OMM_VERS"],
            COMMENT=satelite["spaceTrack"]["COMMENT"],
            CREATION_DATE=satelite["spaceTrack"]["CREATION_DATE"],
            ORIGINATOR=satelite["spaceTrack"]["ORIGINATOR"],
            OBJECT_NAME=satelite["spaceTrack"]["OBJECT_NAME"],
            OBJECT_ID=satelite["spaceTrack"]["OBJECT_ID"],
            CENTER_NAME=satelite["spaceTrack"]["CENTER_NAME"],
            REF_FRAME=satelite["spaceTrack"]["REF_FRAME"],
            TIME_SYSTEM=satelite["spaceTrack"]["TIME_SYSTEM"],
            MEAN_ELEMENT_THEORY=satelite["spaceTrack"]["MEAN_ELEMENT_THEORY"],
            EPOCH=satelite["spaceTrack"]["EPOCH"],
            MEAN_MOTION=satelite["spaceTrack"]["MEAN_MOTION"],
            ECCENTRICITY=satelite["spaceTrack"]["ECCENTRICITY"],
            INCLINATION=satelite["spaceTrack"]["INCLINATION"],
            RA_OF_ASC_NODE=satelite["spaceTrack"]["RA_OF_ASC_NODE"],
            ARG_OF_PERICENTER=satelite["spaceTrack"]["ARG_OF_PERICENTER"],
            MEAN_ANOMALY=satelite["spaceTrack"]["MEAN_ANOMALY"],
            EPHEMERIS_TYPE=satelite["spaceTrack"]["EPHEMERIS_TYPE"],
            CLASSIFICATION_TYPE=satelite["spaceTrack"]["CLASSIFICATION_TYPE"],
            NORAD_CAT_ID=satelite["spaceTrack"]["NORAD_CAT_ID"],
            ELEMENT_SET_NO=satelite["spaceTrack"]["ELEMENT_SET_NO"],
            REV_AT_EPOCH=satelite["spaceTrack"]["REV_AT_EPOCH"],
            BSTAR=satelite["spaceTrack"]["BSTAR"],
            MEAN_MOTION_DOT=satelite["spaceTrack"]["MEAN_MOTION_DOT"],
            MEAN_MOTION_DDOT=satelite["spaceTrack"]["MEAN_MOTION_DDOT"],
            SEMIMAJOR_AXIS=satelite["spaceTrack"]["SEMIMAJOR_AXIS"],
            PERIOD=satelite["spaceTrack"]["PERIOD"],
            APOAPSIS=satelite["spaceTrack"]["APOAPSIS"],
            PERIAPSIS=satelite["spaceTrack"]["PERIAPSIS"],
            OBJECT_TYPE=satelite["spaceTrack"]["OBJECT_TYPE"],
            RCS_SIZE=satelite["spaceTrack"]["RCS_SIZE"],
            COUNTRY_CODE=satelite["spaceTrack"]["COUNTRY_CODE"],
            LAUNCH_DATE=satelite["spaceTrack"]["LAUNCH_DATE"],
            SITE=satelite["spaceTrack"]["SITE"],
            DECAY_DATE=satelite["spaceTrack"]["DECAY_DATE"],
            DECAYED=satelite["spaceTrack"]["DECAYED"],
            FILE=satelite["spaceTrack"]["FILE"],
            GP_ID=satelite["spaceTrack"]["GP_ID"],
            TLE_LINE0=satelite["spaceTrack"]["TLE_LINE0"],
            TLE_LINE1=satelite["spaceTrack"]["TLE_LINE1"],
            TLE_LINE2=satelite["spaceTrack"]["TLE_LINE2"]
            )
        pony.flush()
        if satelite["launch"] == None:
            satelite["launch"] = "null"
        if satelite["version"] == None:
            satelite["version"] = "null"
        db.Satelite(
            spaceTrack = st1,
            launch = satelite["launch"],
            version= satelite["version"],
            height_km= satelite["height_km"],
            latitude= satelite["latitude"],
            longitude= satelite["longitude"],
            velocity_kms= satelite["velocity_kms"],
            id=satelite["id"]
        )
        pony.commit()
