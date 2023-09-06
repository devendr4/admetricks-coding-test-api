from fastapi import APIRouter

from app.dollar.service import fetch_yearly_data, generate_file

router = APIRouter(prefix="/v1/dollar")


@router.get("/{year}")
def get_yearly_dollar_data(year: int):
    return fetch_yearly_data(str(year))


@router.get("/diff/{year}")
def get_dollar_data_varation(year: int, filetype: str = "xlsx"):
    return generate_file(str(year), filetype)
