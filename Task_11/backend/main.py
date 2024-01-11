from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from algosdk.v2client import algod

app = FastAPI()

# Configure Algorand node connection
algod_token = "YOUR_ALGOD_TOKEN"
algod_address = "YOUR_ALGOD_ADDRESS"
algod_client = algod.AlgodClient(algod_token, algod_address)


# endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

#Algorand endpoint
@app.get("/get_account_balance/{address}")
def get_account_balance(address: str):
    try:
        account_info = algod_client.account_info(address)
        balance = account_info.get("amount", 0)
        return {"address": address, "balance": balance}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
