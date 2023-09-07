# Admetricks coding challenge API
To run this project, you may either use Docker or create a virtual environment and install the dependencies yourself:

To create a virtual environment run:

    python -m venv .venv
Activate the virtual environment:

    source  .venv/bin/activate
Install dependencies:

    pip install -r requirements.txt

 Create a .env file with the following contents:

     API_URL=https://mindicador.cl/api/dolar/

Run the server

    uvicorn app.main:app --reload
