from ninja import Schema
from typing import Optional

class VesselInfoOut(Schema):
    imo: Optional[str] = None
    vessel_name: Optional[str] = None
    year_of_build: Optional[int] = None
    flag: Optional[str] = None
    dwt: Optional[float] = None
    teu_capacity: Optional[float] = None
    draft: Optional[float] = None
    loa: Optional[float] = None
    lbp: Optional[float] = None
    breadth_extreme: Optional[float] = None
    breadth_moulded: Optional[float] = None
    vessel_type: Optional[str] = None



class VesselOut(Schema):
    mmsi: str
    info: Optional[VesselInfoOut] = None



class PaginatedVesselOut(Schema):
    total: int
    page: int
    page_size: int
    results: list[VesselOut]



class ErrorOut(Schema):
    detail: str