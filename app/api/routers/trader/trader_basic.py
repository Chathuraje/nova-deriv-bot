from fastapi import APIRouter
from app.api.libraries.trader import trader_basic as trader
from app.api.models.Trader import TraderDB

# Create an instance of APIRouter for this set of trader-related endpoints
router = APIRouter(
    tags=["Trader Basic"]
)

# Endpoint to retrieve a list of traders
@router.get("/get_traders")
async def get_traders():
    return await trader.get_traders()

# Endpoint to create a new trader
@router.post("/create_trader")
async def create_trader(traderDB: TraderDB):
    return await trader.create_trader(traderDB)

# Endpoint to retrieve details of a specific trader
@router.get("/get_trader/{trader_id}")
async def get_trader(trader_id: str):
    return await trader.get_trader(trader_id)

# # Endpoint to update information of a specific trader
# @router.put("/update_trader/{trader_id}")
# async def update_trader(trader_id: str, traderDB: TraderDB):
#     return await trader.update_trader(trader_id, traderDB)

# # Endpoint to delete a specific trader
# @router.delete("/delete_trader/{trader_id}")
# async def delete_trader(trader_id: str):
#     return await trader.delete_trader(trader_id)