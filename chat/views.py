from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import pipeline
import torch

# Setting the thread count globally is good
torch.set_num_threads(1) 

# --- CRITICAL CHANGE: Load the model globally on startup ---
# This ensures all Gunicorn workers have the model ready 
# and the slow loading time is NOT part of the request processing.
try:
    # Use -1 for CPU as you did
    t5_model = pipeline("text2text-generation", model="t5-small", device=-1)
    print("T5 model loaded successfully.")
except Exception as e:
    # Essential for debugging startup issues
    print(f"Error loading T5 model: {e}")
    t5_model = None

# Remove or simplify get_t5 now that the model is global
def get_t5():
    # If loading failed, this will raise an error on request
    if t5_model is None:
        raise Exception("Model not initialized.")
    return t5_model

@api_view(['POST'])
def chat(request):
    data = request.data or {}
    text = data.get("text", "").strip()
    mode = data.get("mode", "").strip()

    if not text:
        return Response({"response": "Veuillez fournir du texte."}, status=400)
    
    # Check if the model is available before trying inference
    if t5_model is None:
         return Response({"error": "Service non disponible (modèle non chargé)."}, status=503)

    try:
        if mode == "translate":
            prompt = f"translate English to French: {text}"
            # Use the global model directly or via the simplified getter
            reply = get_t5()(prompt)[0]["generated_text"]
        elif mode == "summarize":
            prompt = f"summarize: {text}"
            reply = get_t5()(prompt)[0]["generated_text"]
        else:
            return Response({"response": "Mode inconnu"}, status=400)
        return Response({"response": reply})
    except Exception as e:
        # Catch inference-specific errors
        return Response({"error": str(e)}, status=500)
@api_view(['GET'])
def health_check(request):
    if t5_model is not None:
        return Response({"status": "ok", "model_loaded": True})
    else:
        return Response({"status": "error", "model_loaded": False}, status=503)