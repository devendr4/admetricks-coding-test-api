from io import BytesIO

import httpx
import pandas as pd
from fastapi.responses import StreamingResponse

from app.dollar.config import get_settings


def fetch_yearly_data(year: str):
    try:
        response = httpx.get(get_settings().api_url + year)
        data = response.json()["serie"]

        df = pd.DataFrame.from_dict(data)

        df = df.rename(columns={"fecha": "date"})
        df["date"] = pd.to_datetime(df.date)
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

        df["variation"] = round(df["valor"] - df["valor"].shift(-1), 4)
        df = df.fillna(0)
        df = df.drop(columns=["valor"])

        return {"data": df.to_dict(orient="records")}
    except Exception as e:
        print("There was an error while fetching the data")
        print(e)


def generate_file(year: str, filetype: str):
    try:
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
                headers={
                    "Content-Disposition": "attachment;filename=" + filename + ".csv"
                },
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

    except Exception as e:
        print(e)
        print("There was an error while generating the files")
