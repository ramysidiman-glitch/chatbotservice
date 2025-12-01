from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import pipeline

# Utilisation de modèles BEAUCOUP plus légers
# t5-small fait ~240Mo (contre >1Go pour les autres)
# On utilise t5-small pour les DEUX tâches (il est multitâche)
model_name = "t5-small" 

# On charge le pipeline une seule fois pour économiser la RAM
# Note: le chargement au démarrage peut prendre du temps sur Render
pipe = pipeline("text2text-generation", model=model_name)

@api_view(['POST'])
def chat(request):
    text = request.data.get("text", "").strip()
    mode = request.data.get("mode", "").strip()

    if not text:
        return Response({"response": "Veuillez fournir du texte."})

    reply = ""
    try:
        if mode == "translate":
            # T5 utilise des préfixes pour savoir quoi faire
            input_text = f"translate English to French: {text}"
            res = pipe(input_text, max_length=512)
            reply = res[0]['generated_text']

        elif mode == "summarize":
            input_text = f"summarize: {text}"
            res = pipe(input_text, min_length=30, max_length=150)
            reply = res[0]['generated_text']
        else:
            reply = "Mode inconnu"
            
    except Exception as e:
        reply = f"Erreur modèle: {str(e)}"

    return Response({"response": reply})
@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"})
    