from fastapi import APIRouter
from app.api.libraries.trader import trader_activities as trader
from app.api.models.Trader import TraderDB

# Create an instance of APIRouter for this set of trader-related endpoints
router = APIRouter(
    tags=["Trader Activities"]
)

@router.get("/get_trader_copier_status/{trader_id}")
async def get_trader_copier_status(trader_id: str):
    return await trader.get_trader_copier_status(trader_id)

# Endpoint to set a trader as active
@router.put("/set_trader_active/{trader_id}")
async def set_trader_active(trader_id: str):
    return await trader.set_trader_active(trader_id)

# Endpoint to set a trader as inactive
@router.put("/set_trader_inactive/{trader_id}")
async def set_trader_inactive(trader_id: str):
    return await trader.set_trader_inactive(trader_id)

# Endpoint to get all the copier list
@router.get("/get_copier_list/{trader_id}")
async def get_copier_list(trader_id: str):
    return await trader.get_copier_list(trader_id)

# # Endpoint to set all the traders active
# @router.put("/set_all_traders_active")
# async def set_all_traders_active():
#     return await trader.set_all_traders_active()

# # Endpoint to set all the traders inactive
# @router.put("/set_all_traders_inactive")
# async def set_all_traders_inactive():
#     return await trader.set_all_traders_inactive()

# Endpoint to get all the active traders
@router.get("/get_active_traders")
async def get_active_traders():
    return await trader.get_active_traders()







# @router.put("/withdraw_money/{trader_id}")
# async def withdraw_money(trader_id: str):
#     return await trader.withdraw_money(trader_id)