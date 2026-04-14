# api/index.py
from dashboard import main # We will wrap your dashboard
import os

# This satisfies Vercel's "Missing Handler" error
def handler(request):
    return {
        "statusCode": 200,
        "body": "Streamlit is running on a different instance."
    }
