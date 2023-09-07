import traceback
from io import BytesIO

import httpx
import pandas as pd
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from app.usd.config import get_settings
from app.usd.redis import redis_service


def generate_file(df: pd.DataFrame, year: str, filetype: str):
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
    else:
        raise Exception("Invalid filetype")


def fetch_usd_variation(year: str, filetype: str | None):
    try:
        df = redis_service.get(year)
        print("redis", df)
        if df:
            return {"data": df.to_dict(orient="records")}

        response = httpx.get(get_settings().api_url + year)
        response.raise_for_status()
        data = response.json()["serie"]

        if not len(data):
            raise Exception("No data was found")

        df = pd.DataFrame.from_dict(data)

        df = df.rename(columns={"fecha": "date"})

        df["date"] = pd.to_datetime(df.date)
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

        df["variation"] = round(df["valor"] - df["valor"].shift(-1), 4)
        df = df.fillna(0)
        if not filetype:
            df = df.drop(columns=["valor"])

        # if filetype query param is present, generate file
        if filetype:
            return generate_file(df, year, filetype)

        redis_service.set(year, df)

        return {"data": df.to_dict(orient="records")}

    except httpx.HTTPStatusError as e:
        msg = str(e)
        if e.response.json().get("message") == "Fecha incorrecta":
            msg = "Invalid date"
        raise HTTPException(status_code=404, detail=msg)

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=404, detail=str(e))
