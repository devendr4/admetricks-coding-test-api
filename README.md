# CLP to USD rate API
To run this project, you may either use Docker or create a virtual environment and install the dependencies locally.
It's suggested to run it using Docker because of the redis server, otherwise, you'll have to set up a redis server yourself.


 Create a .env file with the following contents:

     API_URL=https://mindicador.cl/api/dolar/

To run the project using Docker:

    docker compose up --build

To run the unit tests using docker:

    docker exec -ti <container id> bash
    pytest

To create a virtual environment run:

    python -m venv .venv
Activate the virtual environment:

    source  .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt


Run the server

    uvicorn app.main:app --reload

Run the tests

    pytest
