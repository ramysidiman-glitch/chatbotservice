from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import pipeline
import torch

torch.set_num_threads(1)  # réduit la consommation RAM

t5_model = None

def get_t5():
    global t5_model
    if t5_model is None:
        t5_model = pipeline("text2text-generation", model="t5-small", device=-1)
    return t5_model

@api_view(['POST'])
def chat(request):
    data = request.data or {}
    text = data.get("text", "").strip()
    mode = data.get("mode", "").strip()

    if not text:
        return Response({"response": "Veuillez fournir du texte."}, status=400)

    try:
        if mode == "translate":
            prompt = f"translate English to French: {text}"
            reply = get_t5()(prompt)[0]["generated_text"]
        elif mode == "summarize":
            prompt = f"summarize: {text}"
            reply = get_t5()(prompt)[0]["generated_text"]
        else:
            return Response({"response": "Mode inconnu"}, status=400)
        return Response({"response": reply})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"})
