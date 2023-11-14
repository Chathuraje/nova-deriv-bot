from pydantic import BaseModel, EmailStr
from app.api.config.hashing import encrypt, decrypt

class TraderDB(BaseModel):
    account_id: str
    name: str
    email: EmailStr
    admin_api_key: str
    read_only_api_key: str
    app_id: str
    status: bool = False
    
    def encrypt_api_keys(self):
        self.admin_api_key = encrypt(self.admin_api_key)
        self.read_only_api_key = encrypt(self.read_only_api_key)

    def decrypt_api_keys(self):
        self.admin_api_key = decrypt(self.admin_api_key)
        self.read_only_api_key = decrypt(self.read_only_api_key)