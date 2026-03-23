from ninja import Router
from django.shortcuts import get_object_or_404
from typing import Optional
from core.models import Vessel, VesselInfo
from core.schemas import VesselOut, PaginatedVesselOut
from ninja import NinjaAPI
from http import HTTPStatus
from core.schemas import VesselOut, PaginatedVesselOut, ErrorOut

router = Router()


@router.get("{mmsi}", response={200: VesselOut, 460: ErrorOut})
def get_vessel(request, mmsi: str):
    try:
        vessel = Vessel.objects.get(mmsi=mmsi)
    except Vessel.DoesNotExist:
        return 460, {"detail": f"Vessel with MMSI {mmsi} not found"}

    info = VesselInfo.objects.filter(mmsi=vessel).first()
    return 200, {
        'mmsi': vessel.mmsi,
        'info': info,
    }


@router.get("", response={200: PaginatedVesselOut, 400: ErrorOut})
def get_vessels(
        request,
        page: int = 1,
        page_size: int = 20,
        vessel_type: Optional[str] = None,
        flag: Optional[str] = None,
        year_of_build: Optional[int] = None,
):
    if page < 1:
        return 400, {"detail": "Page number must be 1 or greater"}
    if page_size < 1 or page_size > 100:
        return 400, {"detail": "Page size must be between 1 and 100"}

    qs = Vessel.objects.select_related('vesselinfo').all()

    if vessel_type:
        qs = qs.filter(vesselinfo__vessel_type__icontains=vessel_type)
    if flag:
        qs = qs.filter(vesselinfo__flag__icontains=flag)
    if year_of_build:
        qs = qs.filter(vesselinfo__year_of_build=year_of_build)

    total = qs.count()
    start = (page - 1) * page_size
    end = start + page_size
    qs = qs[start:end]

    results = []
    for vessel in qs:
        info = getattr(vessel, 'vesselinfo', None)
        results.append({
            'mmsi': vessel.mmsi,
            'info': info,
        })

    return 200, {
        'total': total,
        'page': page,
        'page_size': page_size,
        'results': results,
    }

