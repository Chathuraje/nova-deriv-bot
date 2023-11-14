from bson import ObjectId
from app.api.models.Copier import CopierDB
from app.api.config.database import copier_collection, trader_collection
from app.api.schemas.copierSchema import individual_copier, list_copiers
from app.api.libraries.copier.deriv_copier import (
    deriv_set_copier_active,
    deriv_set_copier_inactive,
    deriv_get_trader_list
)
from app.api.config.hashing import decrypt
import asyncio

async def change_copier_trader(copier_id: str, new_trader_id: str):
    await set_copier_inactive(copier_id)
    
    # check if the copier exists
    copier_exists = copier_collection.find_one({"_id": ObjectId(copier_id)})
    
    if not copier_exists:
        # Return a message indicating that the associated copier doesn't exist
        return "copier does not exist"
    
    # Check if the associated trader exists
    trader_exists = trader_collection.find_one({"_id": ObjectId(new_trader_id)})

    if not trader_exists:
        # Return a message indicating that the associated trader doesn't exist
        return "Trader does not exist"
    
    old_trader_id = copier_exists['trader_id']
    # Remove old trader from copier
    
    # Update the copier in the database and retrieve the updated document
    updated_copier = copier_collection.find_one_and_update(
        {"_id": ObjectId(copier_id)},
        {"$set": {"trader_id": new_trader_id}},
        return_document=True
    )
    
    await set_copier_active(copier_id)
    
    # Return the updated copier details
    return individual_copier(updated_copier)

async def __get_copier_api_key(copier_id: str):
    # Find the copier in the database by ID
    copier = copier_collection.find_one({"_id": ObjectId(copier_id)})
    # Return the copier details
    return decrypt(copier['api_key'])


async def __get_copier_account_id(copier_id: str):
    # Find the copier in the database by ID
    copier = copier_collection.find_one({"_id": ObjectId(copier_id)})
    # Return the copier details
    return copier['account_id']

async def __get_trader_app_id(trader_id: str):
    # Find the trader in the database by ID
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    # Return the trader details
    return trader['app_id']


async def __get_read_only_trader_api_key(copier_exists):
    # get related trader api key
    trader_id = copier_exists['trader_id']
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    
    # get api key from trader
    return decrypt(trader['read_only_api_key'])


async def set_copier_active(copier_id: str):
    
    # check if copier exists
    copier_exists = copier_collection.find_one({"_id": ObjectId(copier_id)})
    
    if not copier_exists:
        # Return a message indicating that the associated trader doesn't exist
        return "copier does not exist"
    
    # check if trader is active or not
    trader_id = copier_exists['trader_id']
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    
    # get the copier api key
    DERIV_TOKEN = await __get_copier_api_key(copier_id)
    APP_ID = await __get_trader_app_id(trader_id)
    read_only_trader_api_key = await __get_read_only_trader_api_key(copier_exists)
    
    # Update the copier in the database and retrieve the updated document
    await deriv_set_copier_active(DERIV_TOKEN, read_only_trader_api_key, APP_ID)
    
    updated_copier = copier_collection.find_one_and_update(
        {"_id": ObjectId(copier_id)},
        {"$set": {"status": True}},
        return_document=True
    )
    # Return the updated copier details
    return "copier set to active"

# async def set_all_copiers_active():
#     # get all copiers
#     copiers = copier_collection.find()
    
#     for copier in copiers:
#         # check if copier is already active
#         if copier['status'] == True:
#             # Return a message indicating that the associated trader doesn't exist
#             return "copier is already active"
        
#         # check if trader is active or not
#         trader_id = copier['trader_id']
#         trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
        
#         if trader['status'] == False:
#             # Return a message indicating that the associated trader doesn't exist
#             return "trader is not active"
        
#         # get the copier api key
#         DERIV_TOKEN = await __get_copier_api_key(copier['_id'])
#         APP_ID = await __get_trader_app_id(trader_id)
#         read_only_trader_api_key = await __get_read_only_trader_api_key(copier)
        
#         # Update the copier in the database and retrieve the updated document
#         await deriv_set_copier_active(DERIV_TOKEN, read_only_trader_api_key, APP_ID)
        
#         updated_copier = copier_collection.find_one_and_update(
#             {"_id": ObjectId(copier['_id'])},
#             {"$set": {"status": True}},
#             return_document=True
#         )
    
#     # Return the updated copier details
#     return "all copiers set to active"

# async def set_all_copiers_inactive():
#     # get all copiers
#     copiers = copier_collection.find()
    
#     for copier in copiers:
#         # check if copier is already active
#         if copier['status'] == False:
#             # Return a message indicating that the associated trader doesn't exist
#             return "copier is already inactive"
        
#         # check if trader is active or not
#         trader_id = copier['trader_id']
#         trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
        
#         if trader['status'] == False:
#             # Return a message indicating that the associated trader doesn't exist
#             return "trader is not active"
        
#         # get the copier api key
#         DERIV_TOKEN = await __get_copier_api_key(copier['_id'])
#         APP_ID = await __get_trader_app_id(trader_id)
#         read_only_trader_api_key = await __get_read_only_trader_api_key(copier)
        
#         # Update the copier in the database and retrieve the updated document
#         await deriv_set_copier_inactive(DERIV_TOKEN, read_only_trader_api_key, APP_ID)
        
#         updated_copier = copier_collection.find_one_and_update(
#             {"_id": ObjectId(copier['_id'])},
#             {"$set": {"status": False}},
#             return_document=True
#         )
    
#     # Return the updated copier details
#     return "all copiers set to inactive"

async def get_active_copiers():
    # get all copiers
    copiers = copier_collection.find({"status": True})
    
    return list_copiers(copiers)


async def get_connected_trader_list(copier_id):
    copier_exists = copier_collection.find_one({"_id": ObjectId(copier_id)})
    trader_id = copier_exists['trader_id']
    
    # Update the trader in the database and retrieve the updated document
    DERIV_TOKEN = await __get_copier_api_key(copier_id)
    APP_ID = await __get_trader_app_id(trader_id)
        
    return await deriv_get_trader_list(DERIV_TOKEN, APP_ID)

async def set_copier_inactive(copier_id: str):
    # check if copier exists
    copier_exists = copier_collection.find_one({"_id": ObjectId(copier_id)})
    trader_id = copier_exists['trader_id']
    
    
    if not copier_exists:
        # Return a message indicating that the associated trader doesn't exist
        return "copier does not exist"
    
    # get the copier api key
    DERIV_TOKEN = await __get_copier_api_key(copier_id)
    APP_ID = await __get_trader_app_id(trader_id)
    
    
    read_only_trader_api_key = await __get_read_only_trader_api_key(copier_exists)
    
    # Update the copier in the database and retrieve the updated document
    await deriv_set_copier_inactive(DERIV_TOKEN, read_only_trader_api_key, APP_ID)
    
    updated_copier = copier_collection.find_one_and_update(
        {"_id": ObjectId(copier_id)},
        {"$set": {"status": False}},
        return_document=True
    )
    # Return the updated copier details
    return "copier set to inactive"
