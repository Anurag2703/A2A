# test_gemini_key.py
import os
import google.generativeai as genai

# Put your key here temporarily just for testing
API_KEY = "AIzaSyCuu16jQLiPDpbUVaZQu9x5NF2N5nVDZ_M"

genai.configure(api_key=API_KEY)

try:
    models = genai.list_models()
    print("✅ Key is valid. Models available:")
    for m in models:
        print("-", m.name)
except Exception as e:
    print("❌ Key test failed:")
    print(e)
