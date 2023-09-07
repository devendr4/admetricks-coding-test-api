from fastapi import APIRouter

from app.usd.service import fetch_usd_variation

router = APIRouter(prefix="/v1/usd")


@router.get("/{year}")
def get_usd_data_varation(year: int, filetype: str | None = None):
    return fetch_usd_variation(str(year), filetype)
