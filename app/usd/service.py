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
        # checks if data is cacached on redis, if it isn't, query API
        # and transform the data
        if (df is None) or df.empty:
            response = httpx.get(get_settings().api_url + year)
            response.raise_for_status()
            data = response.json()["serie"]

            if not len(data):
                raise Exception("No data was found")

            df = pd.DataFrame.from_dict(data)

            df = df.rename(columns={"fecha": "date", "valor": "value"})
            df["date"] = pd.to_datetime(df.date)
            df["date"] = df["date"].dt.strftime("%Y-%m-%d")

            df["variation"] = round(df["value"] - df["value"].shift(-1), 4)
            df = df.fillna(0)

            # save data to redis after transforming it
            redis_service.set(year, df)

        # if filetype query param is present, generate file
        if filetype:
            df["variation_percentage"] = (
                lambda x, y: round((x - y) / ((x + y) / 2) * 100, 3)
            )(df["value"], df["value"].shift(-1))
            return generate_file(df, year, filetype)

        else:
            df = df.drop(columns=["value"])

        return {"data": df.to_dict(orient="records")}

    except httpx.HTTPStatusError as e:
        msg = str(e)
        if e.response.json().get("message") == "Fecha incorrecta":
            msg = "Invalid date"
        raise HTTPException(status_code=404, detail=msg)

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=404, detail=str(e))
