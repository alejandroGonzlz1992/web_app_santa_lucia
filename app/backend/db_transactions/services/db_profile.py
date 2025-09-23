# import
import string, random
from re import compile
from fastapi import HTTPException, status
from typing import Union
from pydantic import BaseModel
from sqlalchemy.orm import Session

from numpy.core.records import record
from sqlalchemy.orm import aliased
from sqlalchemy import or_

# local import
from app.backend.database import models
from app.backend.tooling.setting.constants import Constants as Cns


# class
class Profile_Trans_Manager:

    # init
    def __init__(self):
        self.models = models
        self.status = status
        self.http_exec = HTTPException
        self.cns = Cns

    # querying province, canton, and districts
    async def querying_province_canton_and_districts(
            self, db: Union[Session, BaseModel]) -> dict[object]:

        # provinces
        all_province = db.query(
            self.models.Province.id_record.label('_prov_id'),
            self.models.Province.name.label('_prov_name'),
        ).all()
        province_return = [{"_prov_id": _prov_id, "_prov_name": _prov_name} for _prov_id, _prov_name in all_province]

        # cantons
        all_canton = db.query(
            self.models.Canton.id_record.label('_cant_id'),
            self.models.Canton.name.label('_cant_name'),
            self.models.Canton.id_province.label('_prov_id'),
        ).all()
        canton_return = [{"_cant_id": _cant_id, "_cant_name": _cant_name, "_prov_id": _prov_id}
                         for _cant_id, _cant_name, _prov_id in all_canton]

        # districts
        all_district = db.query(
            self.models.District.id_record.label('_dist_id'),
            self.models.District.name.label('_dist_name'),
            self.models.District.id_canton.label('_cant_id'),
        ).all()
        district_return = [{"_dist_id": _dist_id, "_dist_name": _dist_name, "_cant_id": _cant_id}
                         for _dist_id, _dist_name, _cant_id in all_district]

        # return
        return {"province": province_return, "canton": canton_return, "district": district_return}
