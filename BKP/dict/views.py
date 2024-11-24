from django.shortcuts import render

import pandas as pd

# Create your views here.

df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vT79R5fgLfFdx1_Y9EAI7Kk3ysJ-QfNtsjiu7H1uqwUQ5afvi4L3nj3C6x-M00rWcDJvUYQZx2Sh4uB/pub?gid=0&single=true&output=csv')

def index(request):
    vars = df.query('important == "*"').sample(100).to_numpy().tolist()
    return render(request, 'dict/index.html', {'vars':vars})


def phrases(request):
    zborovi = df.query('important == "*"').sample(10).to_numpy().tolist()

    context_dict = {
        'zborovi':zborovi
    }

    return render(request, 'dict/phrases.html', context_dict)

