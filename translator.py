# translator.py
import requests
import json

def translate_rapidapi(text, source_lang='es', target_lang='en'):
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "x-rapidapi-key": "8af040fa32mshfe22ef56a1e39d9p11b224jsnce1058c0a1eb"
    }
    payload = {"from": source_lang, "to": target_lang, "q": text}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        result = response.json()
        if isinstance(result, list) and result:
            return result[0]
        print("⚠️ Unexpected translation response:", result)
    except Exception as e:
        print("❌ Translation API error:", e)
    return text
