from pydantic import BaseModel, EmailStr
from app.api.config.hashing import encrypt, decrypt

class CopierDB(BaseModel):
    account_id: str
    name: str
    email: EmailStr
    api_key: str
    trader_id: str  # Reference to the TraderDB model
    status: bool = False
    
    def encrypt_api_keys(self):
        self.api_key = encrypt(self.api_key)

    def decrypt_api_keys(self):
        self.api_key = decrypt(self.api_key)
