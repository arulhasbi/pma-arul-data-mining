import os
import json
import pickle
import pandas as pd
from django.shortcuts import render

# track variable change temporary locally
from pma_arul_man191073 import config as glob

"""
to make a home page
"""
def home(request):
    # invoke list of books
    payload = books()
    return render(request, 'index.html', {
        'records': payload['records']
    })

"""
to make a summary page
"""
def summary(request):
    return render(request, 'summary.html')

"""
to make a recommendation page
"""
def recommendation(request):
    return render(request, 'recommendation.html')

"""
to show list of books in the home page
"""
def books():
    # read the data path
    dirname = os.path.dirname(__file__)
    datapath = os.path.join(dirname, "dataset/books_c.csv")
    # read the data csv
    books = pd.read_csv(datapath)
    # chunk the data for simplicity of application demonstration
    books_chunked = books.head(30).to_dict("records")
    print(books_chunked)
    # define the payload
    payload = {
        "records": books_chunked
    }
    # return the payload
    return payload
