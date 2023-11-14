from fastapi import APIRouter
from app.api.libraries.copier import copier_basic as copier
from app.api.models.Copier import CopierDB

# Create an instance of APIRouter for this set of copier-related endpoints
router = APIRouter(
    tags=["Copier Basic"]
)

# Endpoint to retrieve a list of copiers
@router.get("/get_copiers")
async def get_copiers():
    return await copier.get_copiers()

# Endpoint to create a new copier
@router.post("/create_copier")
async def create_copier(copierDB: CopierDB):
    return await copier.create_copier(copierDB)

# Endpoint to retrieve details of a specific copier
@router.get("/get_copier/{copier_id}")
async def get_copier(copier_id: str):
    return await copier.get_copier(copier_id)

# # Endpoint to update information of a specific copier
# @router.put("/update_copier/{copier_id}")
# async def update_copier(copier_id: str, copierDB: CopierDB):
#     return await copier.update_copier(copier_id, copierDB)

# # Endpoint to delete a specific copier
# @router.delete("/delete_copier/{copier_id}")
# async def delete_copier(copier_id: str):
#     return await copier.delete_copier(copier_id)