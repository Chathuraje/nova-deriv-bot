from bson import ObjectId  # Import ObjectId for working with MongoDB ObjectIDs
from app.api.config.database import trader_collection

def individual_copier(copier):
    # Fetch the trader details based on the trader_id
    trader = trader_collection.find_one({"_id": ObjectId(copier["trader_id"])})
    
    return {
        "id": str(copier["_id"]),
        "account_id": copier["account_id"],
        "name": copier["name"],
        "email": copier["email"],
        "account_balance": copier["account_balance"],
        "api_key": copier["api_key"],
        "status": copier["status"],
        "trader": {
            "id": str(trader["_id"]),
            "name": trader["name"],
            "email": trader["email"],
            "admin_api_key": trader["admin_api_key"],
            "read_only_api_key": trader["read_only_api_key"],
            "app_id": trader["app_id"],
            "status": trader["status"],
        } if trader else None  # Return None if no associated trader is found
    }
    
    
def list_copiers(copiers):
    return [individual_copier(copier) for copier in copiers]