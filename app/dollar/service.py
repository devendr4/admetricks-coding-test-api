from io import BytesIO

import httpx
import pandas as pd
from fastapi.responses import StreamingResponse

from app.dollar.config import get_settings


def fetch_yearly_data(year: str):
    response = httpx.get(get_settings().api_url + year)
    data = response.json()["serie"]
    return {"data": data}


def generate_file(year: str, filetype: str):
    response = httpx.get(get_settings().api_url + year)
    data = response.json()["serie"]

    df = pd.DataFrame.from_dict(data)
    # get dollar value from previous date using pandas shift
    # and calculate percentage diff using a lambda function
    df["variacion"] = (lambda x, y: round((x - y) / ((x + y) / 2) * 100, 3))(
        df["valor"], df["valor"].shift(-1)
    )
    df["fecha"] = pd.to_datetime(df.fecha)
    df["fecha"] = df["fecha"].dt.strftime("%d-%m-%Y")
    print(df)

    filename = "usd_clp_rate_history_" + year
    # return either a csv file or an excel file depending
    # on the 'filetype' query param
    if filetype == "csv":
        return StreamingResponse(
            iter([df.to_csv(index=False)]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment;filename=" + filename + ".csv"},
        )

    if filetype == "xlsx":
        buffer = BytesIO()
        with pd.ExcelWriter(buffer) as writer:
            df.to_excel(writer, index=False)
        return StreamingResponse(
            BytesIO(buffer.getvalue()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=" + filename + ".xlsx"
            },
        )
