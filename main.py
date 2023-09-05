import httpx
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    r = httpx.get("https://mindicador.cl/api/dolar/2023")
    data = r.json()
    dolar_data = []
    for i in data["serie"]:
        item = {}
        item["date"] = i["fecha"]
        item["value"] = i["valor"]
        dolar_data.append(item)
        print(i["fecha"], i.get("valor"))
    return {"data": dolar_data}
