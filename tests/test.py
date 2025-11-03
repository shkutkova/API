import os

from dotenv import load_dotenv

load_dotenv()

def test():
    a = os.getenv("BASE_URL")
    print(a)