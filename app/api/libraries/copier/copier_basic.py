from bson import ObjectId
from app.api.models.Copier import CopierDB
from app.api.config.database import copier_collection, trader_collection
from app.api.schemas.copierSchema import individual_copier, list_copiers
from app.api.libraries.copier.deriv_copier import (
    deriv_set_copier_active,
    deriv_set_copier_inactive,
    deriv_get_trader_list,
    deriv_get_account_balance,
)
from app.api.config.hashing import decrypt
import asyncio


# Function to get a list of all copiers
async def get_copiers():
    # Retrieve all copiers from the database and convert to a list
    copiers = list_copiers(copier_collection.find())
    return copiers

# Function to create a new copier
async def create_copier(copier: CopierDB):
    copier.encrypt_api_keys()
    
    # Check if copier already exists in the database based on email or account_id
    copier_exists = copier_collection.find_one({"$or": [{"email": copier.email}, {"account_id": copier.account_id}]})

    if copier_exists:
        # Return a message indicating that the copier already exists
        return "Copier already exists"

    # Check if the associated trader exists
    trader_exists = trader_collection.find_one({"_id": ObjectId(copier.trader_id)})

    if not trader_exists:
        # Return a message indicating that the associated trader doesn't exist
        return "Trader does not exist"
    
    copier.account_balance = await deriv_get_account_balance(decrypt(copier.api_key), trader_exists["app_id"])
    
    # Convert the copier object to a dictionary and insert it into the database
    copier_dict = dict(copier)
    copier_collection.insert_one(copier_dict)
    # Return the newly created copier
    return individual_copier(copier_dict)
    
    # Function to get a specific copier by ID
async def get_copier(copier_id: str):
    # Find the copier in the database by ID
    copier = copier_collection.find_one({"_id": ObjectId(copier_id)})
    # Return the copier details
    return individual_copier(copier)

# Function to update an existing copier by ID
async def update_copier(copier_id: str, copier: CopierDB):
    copier.encrypt_api_keys()
    
    # Check if trader already exists in the database with a different ID
    existing_copier = copier_collection.find_one({"email": copier.email, "_id": {"$ne": ObjectId(copier_id)}})

    if existing_copier:
        # Return a message indicating that the trader already exists with a different ID
        return "Copier with the same email already exists with a different ID"
    
    # Check if trader already exists in the database with a different ID
    existing_copier = copier_collection.find_one({"account_id": copier.account_id, "_id": {"$ne": ObjectId(copier_id)}})

    if existing_copier:
        # Return a message indicating that the trader already exists with a different ID
        return "Copier with the same account id already exists with a different ID"
    
    # Update the copier in the database and retrieve the updated document
    updated_copier = copier_collection.find_one_and_update(
        {"_id": ObjectId(copier_id)},
        {"$set": dict(copier)},
        return_document=True
    )
    # Return the updated copier details
    return individual_copier(updated_copier)

# Function to delete a copier by ID
async def delete_copier(copier_id: str):
    # Find and delete the copier from the database by ID
    copier_collection.find_one_and_delete({"_id": ObjectId(copier_id)})
    # Return a message indicating successful deletion
    return {"message": "copier deleted successfully"}