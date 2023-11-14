from app.api.models.Trader import TraderDB
from app.api.config.database import trader_collection
from app.api.schemas.traderSchema import individual_trader, list_traders
from bson import ObjectId

# Function to get a list of all traders
async def get_traders():
    # Retrieve all traders from the database and convert to a list
    traders = list_traders(trader_collection.find())
    return traders

# Function to create a new trader
async def create_trader(trader: TraderDB):
    # Encrypt API keys before storing in the database
    trader.encrypt_api_keys()
    
    # Check if trader already exists in the database based on email or account_id
    trader_exists = trader_collection.find_one({"$or": [{"email": trader.email}, {"account_id": trader.account_id}]})

    if trader_exists:
        # Return a message indicating that the trader already exists
        return "Trader already exists"
    
    # Convert the trader object to a dictionary and insert it into the database
    trader_dict = dict(trader)
    trader_collection.insert_one(trader_dict)
    # Return the newly created trader
    return individual_trader(trader_dict)
    
# Function to get a specific trader by ID
async def get_trader(trader_id: str):
    # Find the trader in the database by ID
    trader = trader_collection.find_one({"_id": ObjectId(trader_id)})
    # Return the trader details
    return individual_trader(trader)

# Function to update an existing trader by ID
async def update_trader(trader_id: str, trader: TraderDB):
    trader.encrypt_api_keys()
    
    # Check if trader already exists in the database with a different ID
    existing_trader = trader_collection.find_one({"email": trader.email, "_id": {"$ne": ObjectId(trader_id)}})

    if existing_trader:
        # Return a message indicating that the trader already exists with a different ID
        return "Trader with the same email already exists with a different ID"
    
    # Check if trader already exists in the database with a different ID
    existing_trader = trader_collection.find_one({"account_id": trader.email, "_id": {"$ne": ObjectId(trader_id)}})

    if existing_trader:
        # Return a message indicating that the trader already exists with a different ID
        return "Trader with the same account id already exists with a different ID"

    
    # Update the trader in the database and retrieve the updated document
    updated_trader = trader_collection.find_one_and_update(
        {"_id": ObjectId(trader_id)},
        {"$set": dict(trader)},
        return_document=True
    )
    # Return the updated trader details
    return individual_trader(updated_trader)