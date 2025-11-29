from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import requests

# Récupération du token Hugging Face depuis les variables d'environnement

HF_API_KEY = os.environ.get("HF_API_KEY")
HF_API_URL = "[https://api-inference.huggingface.co/models/t5-small](https://api-inference.huggingface.co/models/t5-small)"

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

@api_view(['POST'])
def chat(request):
    data = request.data or {}
    text = data.get("text", "").strip()
    mode = data.get("mode", "").strip()


    if not text:
        return Response({"response": "Veuillez fournir du texte."}, status=400)

    if not HF_API_KEY:
        return Response({"error": "HF_API_KEY non défini"}, status=500)

# Définition du prompt selon le mode
    if mode == "translate":
        payload = {"inputs": f"translate English to French: {text}"}
    elif mode == "summarize":
        payload = {"inputs": f"summarize: {text}"}
    else:
        return Response({"response": "Mode inconnu"}, status=400)

    try:
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
    # Récupération du texte généré
        reply = result[0]["generated_text"] if isinstance(result, list) else str(result)
        return Response({"response": reply})
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def health_check(request):
# Test simple si la clé est présente
    if HF_API_KEY:
        return Response({"status": "ok", "model_loaded": True})
    else:
        return Response({"status": "error", "model_loaded": False}, status=503)
