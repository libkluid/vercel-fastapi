from os import environ
from supabase import create_client, Client

def supabase_client() -> Client:
    url: str = environ.get("SUPABASE_URL")
    key: str = environ.get("SUPABASE_KEY")
    return create_client(url, key)
