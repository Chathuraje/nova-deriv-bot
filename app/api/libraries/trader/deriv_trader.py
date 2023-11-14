import sys
import os
from deriv_api import DerivAPI
from app.api.config.database import copier_collection, trader_collection
from bson import ObjectId
from app.api.config.hashing import decrypt

async def __initialize_api(APP_ID):
    # Initialize Deriv API
    api = DerivAPI(app_id=APP_ID)

    return api

async def __authorize_with_token(api, token):
    # Authorize with API token
    authorize = await api.authorize(token)
   
    return authorize

async def deriv_set_trader_active(DERIV_TOKEN, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    set_settings_args = {
        "allow_copiers": 1,
    }
    await api.set_settings(set_settings_args)
    await api.clear()
    
async def deriv_set_trader_inactive(DERIV_TOKEN, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    set_settings_args = {
        "allow_copiers": 0,
    }
    await api.set_settings(set_settings_args)
    await api.clear()
    

async def deriv_get_trader_copier_status(DERIV_TOKEN, TRADER_ID, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    copytrading_statistics_args = {
        "copytrading_statistics": 1,
        "trader_id": TRADER_ID
    }
    
    data = await api.copytrading_statistics(copytrading_statistics_args)
    await api.clear()
    
    return data


async def deriv_get_copier_list(DERIV_TOKEN, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    copytrading_list_args = {
        "copytrading_list": 1
    }
    
    data = await api.copytrading_list(copytrading_list_args)
    await api.clear()
    
    return data
    
    
    

async def __get_account_list_to_withdraw_money(DERIV_TOKEN, APP_ID):
    # Run the sample calls
    list = await deriv_get_copier_list(DERIV_TOKEN, APP_ID)
    copiers_list = list["copytrading_list"]["copiers"]
    
    
    merged_data = []
    for copier in copiers_list:
        cop = copier["loginid"]
        copier_exists = copier_collection.find_one({"account_id": cop})

        if copier_exists:
            # Extract the value associated with the '_id' key
            merged_info = str(copier_exists['_id'])
            merged_data.append(merged_info)

    return merged_data
    
    
# async def __withdraw_individual(account, trader_id) :
#     trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    
#     account = copier_collection.find_one({"_id": ObjectId(account)})
#     api = await __initialize_api(trader['app_id'])
#     await __authorize_with_token(api, account['api_key'])
    
    
#     p2p_order_create_args = {
#         "p2p_order_create": 1,
#         "advert_id": "1234",
#         "amount": 100
#     }
#     api.p2p_order_create(p2p_order_create_args)
    
#     return "Withdrawn", "100"
    
    
    
    
# async def deriv_withdraw_money(DERIV_TOKEN, APP_ID, trader_id):
    
#     account_list = await __get_account_list_to_withdraw_money(DERIV_TOKEN, APP_ID)
#     merged_data = []
        
#     for account in account_list:
#         result, amount = await __withdraw_individual(account, trader_id)
#         merged_info = {
#             '_id': account,  # Convert ObjectId to string
#             'result': result,
#             'amount': amount,
#         }
#         merged_data.append(merged_info)

#     return merged_data
        