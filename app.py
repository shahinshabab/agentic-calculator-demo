import os

import psycopg
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from calculator import CalculatorError, calculate


app = FastAPI(title="Orange Theme Calculator", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
database_url = os.environ["DATABASE_URL"]


class CalculationRequest(BaseModel):
    expression: str = Field(min_length=1, max_length=100)


def initialize_database():
    with psycopg.connect(database_url) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS calculation_history (
                id BIGSERIAL PRIMARY KEY,
                expression VARCHAR(100) NOT NULL,
                result DOUBLE PRECISION NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            """
        )


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/health")
def health():
    with psycopg.connect(database_url) as connection:
        connection.execute("SELECT 1").fetchone()
    return {"status": "healthy", "service": "agentic-calculator"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "product_name": "Orange Theme Calculator",
            "tagline": "A clear, modern calculator with a warm orange interface.",
        },
    )


@app.post("/api/calculate")
def calculate_expression(payload: CalculationRequest):
    try:
        result = calculate(payload.expression)
    except CalculatorError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    with psycopg.connect(database_url) as connection:
        connection.execute(
            "INSERT INTO calculation_history (expression, result) VALUES (%s, %s)",
            (payload.expression, result),
        )
    return {"expression": payload.expression, "result": result}


@app.get("/api/history")
def history():
    with psycopg.connect(database_url) as connection:
        rows = connection.execute(
            """
            SELECT expression, result, created_at
            FROM calculation_history ORDER BY id DESC LIMIT 8
            """
        ).fetchall()
    return [
        {
            "expression": row[0],
            "result": row[1],
            "created_at": row[2].isoformat(),
        }
        for row in rows
    ]

