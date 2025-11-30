from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import requests

# URL du modèle Hugging Face léger et compatible API gratuite

HF_API_URL = "https://api-inference.huggingface.co/models/google/mt5-small"
HF_API_KEY = os.environ.get("HF_API_KEY")

# Header pour l'authentification

HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}

@api_view(['POST'])
def chat(request):
    data = request.data or {}
    text = data.get("text", "").strip()
    mode = data.get("mode", "").strip()

    if not text:
        return Response({"response": "Veuillez fournir du texte."}, status=400)

    if not HF_API_KEY:
        return Response({"error": "HF_API_KEY non défini"}, status=500)

    # Construire le prompt selon le mode choisi
    if mode == "translate":
        payload = {"inputs": f"translate English to French: {text}"}
    elif mode == "summarize":
        payload = {"inputs": f"summarize: {text}"}
    else:
        return Response({"response": "Mode inconnu"}, status=400)

    try:
        # Appel à l'API Hugging Face
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        # Récupérer le texte généré
        reply = result[0]["generated_text"] if isinstance(result, list) else str(result)
        return Response({"response": reply})
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def health_check(request):
    # Vérifier que la clé HF est définie
    if HF_API_KEY:
        return Response({"status": "ok", "model_loaded": True})
    else:
        return Response({"status": "error", "model_loaded": False}, status=503)
