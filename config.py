import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key securely
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Model config
MODEL = "gpt-4o-mini"