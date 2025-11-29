from rest_framework.decorators import api_view
from rest_framework.response import Response


summarizer = None
translator = None

@api_view(['POST'])
def chat(request):
    text = request.data.get("text", "").strip()
    mode = request.data.get("mode", "").strip()  # "translate" ou "summarize"

    if not text:
        return Response({"response": "Veuillez fournir du texte."})

    # Limiter le texte à 500 mots pour éviter une explosion mémoire
    text = " ".join(text.split()[:500])

    if mode == "translate":
        if translator is None:
            from transformers import pipeline
            # Modèle léger de traduction EN->FR
            translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr", device=-1)
        reply = translator(text)[0]['translation_text']

    elif mode == "summarize":
        if summarizer is None:
            from transformers import pipeline
            # Modèle léger pour résumé
            summarizer = pipeline("summarization", model="facebook/bart-small-cnn", device=-1)

        if len(text.split()) < 10:
            reply = " ".join(text.split()[:10]) + " ..."
        else:
            words = len(text.split())
            max_len = min(140, words)
            min_len = min(70, max_len)
            reply = summarizer(text, min_length=min_len, max_length=max_len, do_sample=False)[0]['summary_text']

    else:
        reply = "Mode inconnu"

    return Response({"response": reply})
