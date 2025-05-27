import motor.motor_asyncio
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Read the MongoDB URI and DB name from .env
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "inventorydb")  # fallback default

# Create an async MongoDB client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

# Get a reference to the database
db = client[DATABASE_NAME]
