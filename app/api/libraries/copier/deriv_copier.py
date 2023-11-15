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



async def deriv_get_account_balance(DERIV_TOKEN, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    balance_args = {
        "balance": 1
    }
    
    data = await api.balance(balance_args)
    await api.clear()
    
    return data['balance']['balance']


async def __deriv_get_add_account_id(DERIV_TOKEN, APP_ID, withdrawal_account):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    account_list_args =    {
        "p2p_advert_list": 1,
        "counterparty_type": "sell",
        "advertiser_name": withdrawal_account,
    }
    
    account_list = await api.p2p_advert_list(account_list_args)
    await api.clear()
    
    return account_list.get('p2p_advert_list', {}).get('list', [{}])[0].get('id', None)



async def __create_a_payment_method(DERIV_TOKEN, APP_ID):
    # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    
    p2p_advertiser_payment_methods_args = {
        "p2p_advertiser_payment_methods": 1,
        "create": [
            {
            "account": "Transfer to Main Trader for Commision",
            "instructions": "109192830435066",
            "name": "P2P Orders",
            "method": "other"
            }
        ],
    }
    
    p2p_advertiser_payment_methods_args_if_acccount_available = {
        "p2p_advertiser_payment_methods": 1,
    }
        
    p2p_advertiser_payment_methods_data = ""
    try:
        p2p_advertiser_payment_methods_data = await api.p2p_advertiser_payment_methods(p2p_advertiser_payment_methods_args)
    except:
        p2p_advertiser_payment_methods_data = await api.p2p_advertiser_payment_methods(p2p_advertiser_payment_methods_args_if_acccount_available)
    
    await api.clear()
    
    for block_id, block_data in p2p_advertiser_payment_methods_data.get('p2p_advertiser_payment_methods', {}).items():
        if block_data.get('display_name') == 'Other' and block_data.get('fields', {}).get('instructions', {}).get('value') == '109192830435066':
            desired_id = block_id
            break
    
    return desired_id

async def deriv_withdraw(DERIV_TOKEN, APP_ID, amount, withdrawal_account):
    ad_id = await __deriv_get_add_account_id(DERIV_TOKEN, APP_ID, withdrawal_account)
    desired_id = await __create_a_payment_method(DERIV_TOKEN, APP_ID)
    
    # # Run the sample calls
    api = await __initialize_api(APP_ID)
    await __authorize_with_token(api, DERIV_TOKEN)
    
    p2p_order_create_args = {
        "p2p_order_create": 1,
        "advert_id": ad_id,
        "amount": amount,
        "payment_method_ids": [desired_id],
        "contact_info": "0779681281"
        
    }
    
    result = await api.p2p_order_create(p2p_order_create_args)
    await api.clear()
    
    return result