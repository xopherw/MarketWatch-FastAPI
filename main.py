from fastapi import FastAPI, HTTPException
from typing import List, Optional
from marketwatch import marketwatch as MW
from error import Error

app = FastAPI()

@app.get("/stock/{symbol}")
async def get_symbol(symbol: str):
    data = MW(symbol).data()
    json_data = {
        "initiate"  :   "Inidivisual stock data.",
        "symbol"    :   f"{symbol}".upper(),
        "metadata"  :   data
        }
    if(data == 500):
        return Error.connection_error()
    elif(data == 400):
        return Error.bad_request('symbol')
    else:
        return json_data

@app.get("/stock/financial/{symbol}")
async def get_finance(symbol: str, finance: Optional[str] = 'income', interval: Optional[str] = 'annual'):
    data = MW(symbol).financial_data(finance, interval)
    json_data = {
        "initiate"  :   "Inidivisual stock financial data.",
        "symbol"    :   f"{symbol}".upper(),
        "metadata"  :   data
    }
    if(data == 500):
        return Error.connection_error()
    elif(data == 400):
        return Error.ca('symbol')
    else:
        return json_data