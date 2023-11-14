from fastapi import APIRouter
from app.api.libraries.copier import copier_activities as copier
from app.api.models.Copier import CopierDB

# Create an instance of APIRouter for this set of copier-related endpoints
router = APIRouter(
    tags=["Copier Activities"]
)

# Endpoint to create a new copier
@router.post("/change_copier_trader")
async def change_copier_trader(copier_id: str, new_trader_id: str):
    return await copier.change_copier_trader(copier_id, new_trader_id)

@router.put("/update_account_balance/{copier_id}")
async def update_account_balance(copier_id: str):
    return await copier.update_account_balance(copier_id)


# Endpoint to set a copier as active
@router.put("/set_copier_active/{copier_id}")
async def set_copier_active(copier_id: str):
    return await copier.set_copier_active(copier_id)

# Endpoint to set a copier as inactive
@router.put("/set_copier_inactive/{copier_id}")
async def set_copier_inactive(copier_id: str):
    return await copier.set_copier_inactive(copier_id)

# # Endpoint to set all the copiers active
# @router.put("/set_all_copiers_active")
# async def set_all_copiers_active():
#     return await copier.set_all_copiers_active()

# # Endpoint to set all the copiers inactive
# @router.put("/set_all_copiers_inactive")
# async def set_all_copiers_inactive():
#     return await copier.set_all_copiers_inactive()

# Endpoint to get all the active copiers
@router.get("/get_active_copiers")
async def get_active_copiers():
    return await copier.get_active_copiers()

# Endpoint to get all the connected trader
@router.get("/get_connected_trader_list/{copier_id}")
async def get_connected_trader_list(copier_id: str):
    return await copier.get_connected_trader_list(copier_id)