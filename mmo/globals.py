import os
import dotenv

_success = dotenv.load_dotenv()
if not _success:
    raise Exception("Failed to load .env file")

DATABASE = "data/users.json"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # One day

PREFIX = "/api/v1"

# DO NOT USE THESE AS YOUR USERNAME. THEY ARE RESERVED FOR TESTING PURPOSES. I WILL DELETE THEM IF I SEE THEM.
RESERVED_USERNAMES = [
    "test"
]
