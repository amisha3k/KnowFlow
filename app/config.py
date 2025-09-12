
import os


try:
    from dotenv import load_dotenv
    load_dotenv()  # Loads .env if running locally
except ImportError:
    pass  

EURI_API_KEY = os.getenv("EURI_API_KEY")

if not EURI_API_KEY:
    raise ValueError("EURI_API_KEY is missing! Set it in your environment or Hugging Face secrets.")
