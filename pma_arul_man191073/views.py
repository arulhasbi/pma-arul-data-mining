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
    # invoke list of users
    payload = users()
    return render(request, 'index.html', {
        "records": payload["records"]
    })

"""
to make a summary page
"""
def summary(request):
    # invoke ratings data
    payload = ratings()
    return render(request, 'summary.html', {
        "records": payload["records"]
    })

"""
to make a recommendation page
"""
def recommendation(request):
    param = request.GET.get('UID', '')
    param = int(param)
    payload = get_recommendation(param)
    return render(request, 'recommendation.html', {
        'records': payload['records'],
        'user_id': param
    })

"""
to show list of available users in the home page
"""
def users():
    # read the data path
    dirname = os.path.dirname(__file__)
    datapath = os.path.join(dirname, "dataset/py_users_selected.csv")
    # read the data csv
    users = pd.read_csv(datapath)
    users.drop("Unnamed: 0", axis=1, inplace=True)
    users.rename(columns={
        "#BooksRated": "BooksRated"
    }, inplace=True)
    users_to_records = users.to_dict("records")
    # define the payload
    payload = {
        "records": users_to_records
    }
    # return the payload
    return payload

"""
to make books recommendation for a user (books that haven't been rated)
"""
def get_recommendation(UserID):
    # read the data path
    dirname = os.path.dirname(__file__)
    datapath = os.path.join(dirname, "dataset/py_books.csv")
    # read the data csv
    books = pd.read_csv(datapath)
    books.drop("Unnamed: 0", axis=1, inplace=True)
    # read the model path
    modelpath = os.path.join(dirname, "books-recommendation.model")

    import turicreate as tc
    # load the trained model
    model = tc.load_model(modelpath)
    recommendation = make_recommendation(UserID, 6, model, books)
    recommendation_to_records = recommendation.to_dict("records")

    # define the payload
    payload = {
        "records": recommendation_to_records
    }

    # return the payload
    return payload

"""
to get final selected ratings data
"""
def ratings():
    # read the data path
    dirname = os.path.dirname(__file__)
    datapath = os.path.join(dirname, "dataset/py_ratings_used.csv")
    # read the data csv
    ratings = pd.read_csv(datapath)
    ratings.drop("Unnamed: 0", axis=1, inplace=True)
    # get value counts of each of rating scale
    rating_value_counts = pd.DataFrame(ratings["BookRating"].value_counts())
    rating_value_counts.reset_index(inplace=True)
    rating_value_counts.rename(columns={
        "index": "BookRating",
        "BookRating": "Counts"
    }, inplace=True)
    rating_value_counts_to_records = rating_value_counts.to_dict("records")
    print(rating_value_counts)
    # define the payload
    payload = {
        "records": json.dumps(rating_value_counts_to_records)
    }

    return payload

"""
to make a recommendation with parameters of UserID, n, model, and books
"""
def make_recommendation(UserID, n, model, books):
    data = { "ISBN":[] }
    for ISBN in model.recommend(users=[UserID], k=n)["item_id"]:
        data["ISBN"].append(ISBN)
    recommendation = pd.DataFrame(data).merge(books, on="ISBN", how="inner")
    return recommendation
