import google.generativeai as genai
import json

def list_gemini_models(api_key):
    try:
        genai.configure(api_key=api_key)
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)
        return models
    except Exception as e:
        return [str(e)]

if __name__ == "__main__":
    key = "AIzaSyAcTLrFJND4zfFNeINcbSr-yfWh-jwtyQg"
    available_models = list_gemini_models(key)
    print("--- MODELOS DISPONIBLES PARA TU CLAVE ---")
    for model in available_models:
        print(model)
    print("-----------------------------------------")
