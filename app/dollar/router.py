from fastapi import APIRouter

from app.dollar.service import fetch_yearly_data, generate_file

router = APIRouter(prefix="/dollar")


@router.get("/{year}")
def get_yearly_dollar_data(year):
    return fetch_yearly_data(year)


@router.get("/diff/{year}")
def get_dollar_data_varation(year: int, filetype: str = "xlsx"):
    return generate_file(year, filetype)
