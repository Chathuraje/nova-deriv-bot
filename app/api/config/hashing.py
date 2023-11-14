from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

# Constants
SECRET_KEY = os.getenv('SECRET_KEY', '')
cipher_suite = Fernet(SECRET_KEY)

def encrypt(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt(data):
    return cipher_suite.decrypt(data.encode()).decode()

