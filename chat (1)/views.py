import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
HF_API_KEY = os.environ.get("HF_API_KEY")

@api_view(['POST'])
def chat(request):
    text = request.data.get("text", "").strip()
    mode = request.data.get("mode", "").strip()

    if not text:
        return Response({"response": "Veuillez fournir du texte."})

    if mode == "translate":
        data = {"inputs": text}
        result = requests.post(
            "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fr",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            json=data
        ).json()
        reply = result[0]["translation_text"]

    elif mode == "summarize":
        data = {"inputs": text, "parameters": {"min_length": 70, "max_length": 140}}
        result = requests.post(
            "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-6-6",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            json=data
        ).json()
        reply = result[0]["summary_text"]

    else:
        reply = "Mode inconnu"

    return Response({"response": reply})
