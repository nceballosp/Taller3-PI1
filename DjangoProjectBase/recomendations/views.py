from django.shortcuts import render
from movie.models import Movie
from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
# Create your views here.

def get_embedding(text, client, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recommendations(request):
    req = request.GET.get('inputRecom') 
    if req:
        _ = load_dotenv('../openAI.env')
        client = OpenAI(
        # This is the default and can be omitted
            api_key=os.environ.get('openAI_api_key'),
        )
        items = Movie.objects.all()
        emb_req = get_embedding(req, client)
        sim = []
        for i in range(len(items)):
                emb = items[i].emb
                emb = list(np.frombuffer(emb))
                sim.append(cosine_similarity(emb,emb_req))
        sim = np.array(sim)
        print(sim)
        idx = np.argmax(sim)
        idx = int(idx)
        print(idx)
        recom = items[idx].title
        items = Movie.objects.filter(title__icontains=recom)
    else:
        items = Movie.objects.all()
    return render(request, 'recommendations.html', {'searchTerm':req, 'movies':items})




