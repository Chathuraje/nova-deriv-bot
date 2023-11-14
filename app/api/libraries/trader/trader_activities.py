from app.api.models.Trader import TraderDB
from app.api.config.database import trader_collection
from app.api.schemas.traderSchema import individual_trader, list_traders
from bson import ObjectId
from app.api.libraries.trader.deriv_trader import (
    deriv_set_trader_active, 
    deriv_set_trader_inactive, 
    deriv_get_trader_copier_status, 
    deriv_get_copier_list,
    # deriv_withdraw_money
)
from app.api.config.hashing import decrypt

async def __get_trader_admin_api_key(trader_id: str):
    # Find the trader in the database by ID
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    # Return the trader details
    return decrypt(trader['admin_api_key'])

async def __get_trader_account_id(trader_id: str):
    # Find the trader in the database by ID
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    # Return the trader details
    return trader['account_id']

async def __get_trader_app_id(trader_id: str):
    # Find the trader in the database by ID
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    # Return the trader details
    return trader['app_id']

async def set_trader_active(trader_id: str):
    # check if the trader is exists
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    
    if not trader:
        return "Trader not found"
    
    # Update the trader in the database and retrieve the updated document
    DERIV_TOKEN = await __get_trader_admin_api_key(trader_id)
    APP_ID = await __get_trader_app_id(trader_id)
    
    await deriv_set_trader_active(DERIV_TOKEN, APP_ID)
    updated_trader = trader_collection.find_one_and_update(
        {"_id": ObjectId(trader_id)},
        {"$set": {"status": True}},
        return_document=True
    )
        
    return "Trader set to active"

async def set_trader_inactive(trader_id: str):
    
    # check if the trader is exists
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    
    if not trader:
        return "Trader not found"
    
    # Update the trader in the database and retrieve the updated document
    DERIV_TOKEN = await __get_trader_admin_api_key(trader_id)
    APP_ID = await __get_trader_app_id(trader_id)
    
    await deriv_set_trader_inactive(DERIV_TOKEN, APP_ID)
    updated_trader = trader_collection.find_one_and_update(
        {"_id": ObjectId(trader_id)},
        {"$set": {"status": False}},
        return_document=True
    )

    # Return the updated trader details
    return "Trader set to inactive"

async def set_all_traders_active():
    # Retrieve all traders from the database and convert to a list
    traders = list_traders(trader_collection.find())
    
    for trader in traders:
        # check if the trader is already active
        if trader['status'] == True:
            continue
        
        # Update the trader in the database and retrieve the updated document
        DERIV_TOKEN = await __get_trader_admin_api_key(trader['_id'])
        APP_ID = await __get_trader_app_id(trader['_id'])
        
        await deriv_set_trader_active(DERIV_TOKEN, APP_ID)
        updated_trader = trader_collection.find_one_and_update(
            {"_id": ObjectId(trader['_id'])},
            {"$set": {"status": True}},
            return_document=True
        )
    
    return "All traders set to active"

async def get_active_traders():
    # Retrieve all traders from the database and convert to a list
    traders = list_traders(trader_collection.find({"status": True}))
    return traders


async def set_all_traders_inactive():
    # Retrieve all traders from the database and convert to a list
    traders = list_traders(trader_collection.find())
    
    for trader in traders:
        # check if the trader is already active
        if trader['status'] == False:
            continue
        
        # Update the trader in the database and retrieve the updated document
        DERIV_TOKEN = await __get_trader_admin_api_key(trader['_id'])
        APP_ID = await __get_trader_app_id(trader['_id'])
        
        await deriv_set_trader_inactive(DERIV_TOKEN, APP_ID)
        updated_trader = trader_collection.find_one_and_update(
            {"_id": ObjectId(trader['_id'])},
            {"$set": {"status": False}},
            return_document=True
        )
    
    return "All traders set to inactive"


async def get_trader_copier_status(trader_id: str):
    DERIV_TOKEN = await __get_trader_admin_api_key(trader_id)
    TRADER_ID = await __get_trader_account_id(trader_id)
    APP_ID = await __get_trader_app_id(trader_id)

    try:
        data = await deriv_get_trader_copier_status(DERIV_TOKEN, TRADER_ID, APP_ID)
    except:
        data = "Account is not set for copy trading"
    
    return data

# Function to get all the active copier
async def get_copier_list(trader_id: str):
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    
    # Update the trader in the database and retrieve the updated document
    DERIV_TOKEN = await __get_trader_admin_api_key(trader['_id'])
    APP_ID = await __get_trader_app_id(trader['_id'])
        
    return await deriv_get_copier_list(DERIV_TOKEN, APP_ID)









# async def withdraw_money(trader_id: str):
    
#     trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
#     DERIV_TOKEN = await __get_trader_admin_api_key(trader['_id'])
#     APP_ID = await __get_trader_app_id(trader['_id'])
    
#     return await deriv_withdraw_money(DERIV_TOKEN, APP_ID, trader_id)
