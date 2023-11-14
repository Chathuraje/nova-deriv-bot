def individual_trader(trader):
    return {
        "id": str(trader["_id"]),
        "account_id": trader["account_id"],
        "name": trader["name"],
        "email": trader["email"],
        "admin_api_key": trader["admin_api_key"],
        "read_only_api_key": trader["read_only_api_key"],
        "app_id": trader["app_id"],
        "status": trader["status"],
    }
    
    
def list_traders(traders):
    return [individual_trader(trader) for trader in traders]