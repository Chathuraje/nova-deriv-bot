import sys
import os
from deriv_api import DerivAPI

async def __initialize_api(APP_ID):
    # Initialize Deriv API
    api = DerivAPI(app_id=APP_ID)

    # Ping the API
    response = await api.ping({'ping': 1})
    if response['ping']:
        print("Connection established")

    return api

async def __authorize_with_token(api, token):
    # Authorize with API token
    authorize = await api.authorize(token)
   
    return authorize


async def deriv_set_copier_active(DERIV_TOKEN, read_only_trader_api_key, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    set_settings_args = {
        "allow_copiers": 0,
    }
    await api.set_settings(set_settings_args)
    
    copy_start_args = {
        'copy_start': read_only_trader_api_key,
    }
    
    await api.copy_start(copy_start_args)
    await api.clear()
    
async def deriv_set_copier_inactive(DERIV_TOKEN, read_only_trader_api_key, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    copy_stop_args = {
        'copy_stop': read_only_trader_api_key,
    }
    
    await api.copy_stop(copy_stop_args)
    await api.clear()


async def deriv_get_trader_list(DERIV_TOKEN, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    copytrading_list_args = {
        "copytrading_list": 1
    }
    
    data = await api.copytrading_list(copytrading_list_args)
    await api.clear()
    
    return data