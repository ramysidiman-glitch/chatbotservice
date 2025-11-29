from rest_framework.decorators import api_view
from rest_framework.response import Response
from transformers import pipeline

def get_summarizer():
    global summarizer
    if summarizer is None:
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
    return summarizer

def get_translator():
    global translator
    if translator is None:
        translator = pipeline("translation_en_to_fr", model="Helsinki-NLP/opus-mt-en-fr")
    return translator

@api_view(['POST'])
def chat(request):
    # Make sure we read JSON safely
    data = request.data if request.data else {}
    text = data.get("text", "").strip()
    mode = data.get("mode", "").strip()

    if not text:
        return Response({"response": "Veuillez fournir du texte."}, status=400)

    if mode == "translate":
        reply = get_translator()(text)[0]['translation_text']
    elif mode == "summarize":
        words = len(text.split())
        max_len = min(140, words)
        min_len = min(70, max_len)
        reply = get_summarizer()(text, min_length=min_len, max_length=max_len, do_sample=False)[0]['summary_text']
    else:
        return Response({"response": "Mode inconnu"}, status=400)

    return Response({"response": reply})


