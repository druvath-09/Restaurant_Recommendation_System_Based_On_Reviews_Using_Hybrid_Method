from django.shortcuts import render,redirect
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity#used to recommend closed to restaurant
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import joblib
from AdminApp import Database
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request,'index.html')

def AlogAction(request):
    username=request.POST['username']
    password=request.POST['password']

    if username=='Admin' and password=='Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'msg':'Admin Login Failed..!!!'}
        return render(request,'index.html',context)

def Upload(request):
    return render(request,'AdminApp/Upload.html')

global restaurants_data,reviews_data
def UploadAction(request):
    global restaurants_data,reviews_data
    if request.method=="POST":
        f=request.FILES['dataset1'].name
        ff=request.FILES['dataset2'].name
        if f=='Restaurant names.csv' and ff=='Restaurant reviews.csv':
            filename=request.FILES['dataset1']
            restaurants_data=pd.read_csv(filename)

            filename2=request.FILES['dataset2']
            reviews_data=pd.read_csv(filename2)

            context={'msg':'Two Datasets Uploaded Successfully..!!'}
            return render(request,'AdminApp/Upload.html',context)
        else:
            context={'msg':'Please choose Restaurant Names.csv as First then Restaurant reviews.csv'}
            return render(request,'AdminApp/Upload.html',context)
# Preprocess review data
# Ensure Rating column is numeric
def preprocess_ratings(reviews_data):
    reviews_data['Rating'] = pd.to_numeric(reviews_data['Rating'], errors='coerce')
    return reviews_data.dropna(subset=['Rating'])

global reviews_data,restaurants_data
def predatasets(request):
    global reviews_data,restaurants_data
    #first dataset
    rdata=r"Datasets/Restaurant names.csv"
    restaurants_data=pd.read_csv(rdata)
    restaurants_data.isnull().sum()
    restaurants_data.dropna(inplace=True)
    #second dataset
    rrata=r"Datasets/Restaurant reviews.csv"
    reviews_data=pd.read_csv(rrata)
    reviews_data.isnull().sum()
    reviews_data.dropna(inplace=True)

    # Preprocess review data
    reviews_data = preprocess_ratings(reviews_data)

    context={'msg':'Datasets Successfully Preprocessed..!!'}
    return render(request,'AdminApp/Preprocess.html',context)

# Sentiment Analysis
def analyze_sentiment(reviews):
    sia = SentimentIntensityAnalyzer()
    reviews['sentiment_score'] = reviews['Review'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
    return reviews

def SentimentScore(request):
    global reviews_data
    reviews_data = analyze_sentiment(reviews_data)
    table = "<table  class='table'><thead  class='thead-dark'>" \
            "<tr>" \
            "<th scope='col'>Restaurant</th>" \
            "<th scope='col'>Review</th>" \
            "<th scope='col'>Rating</th>" \
            "<th scope='col'>Sentiment Score</th>" \
            "</tr></thead>"


    # Iterate over the rows of the DataFrame
    for _, row in reviews_data.head(3).iterrows():
        table += f"""
                <tbody><tr>
                <td>{row['Restaurant']}</td>
                <td>{row['Review']}</td>
                <td>{row['Rating']}</td>
                <td>{row['sentiment_score']}</td>
                </tr></tbody>
            """
        # Close the table
    table += "</table>"

    # Output or save the HTML table
    with open("reviews_table.html", "w", encoding="utf-8") as file:
        file.write(table)
    context={'data':table,'msg':'Similarity Score Identified Based on Review Column ..!!'}
    return render(request,'AdminApp/Similarity.html',context)

def recommend_context(food_item, data_merged, top_n=5):
    # Create a combined attribute column for context
    data_merged['Attributes'] = data_merged[['Cuisines', 'Collections']].fillna('').apply(' '.join, axis=1)

    # Create TF-IDF matrix for attributes
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(data_merged['Attributes'])

    # Find restaurants that match the food item
    food_item_vector = vectorizer.transform([food_item])
    similarity_scores = cosine_similarity(food_item_vector, tfidf_matrix).flatten()

    # Sort by similarity score
    data_merged['similarity'] = similarity_scores
    recommendations = data_merged.sort_values('similarity', ascending=False).head(top_n)

    return recommendations[['Restaurant', 'Cuisines', 'Cost', 'Timings', 'similarity', 'Rating']]

def train_collaborative_model(reviews_data):
    # Prepare data for Surprise library
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(reviews_data[['Reviewer', 'Restaurant', 'Rating']], reader)
    trainset, _ = train_test_split(data, test_size=0.2)

    # Train the SVD model
    model = SVD()
    model.fit(trainset)
    joblib.dump(model, "Model/svd_model.joblib")
    return model

def recommend_collaborative(user_id, reviews_data, restaurants_data, top_n=5):
    model = joblib.load("Model/svd_model.joblib")
    all_restaurants = restaurants_data['Restaurant'].unique()
    rated_restaurants = reviews_data[reviews_data['Reviewer'] == user_id]['Restaurant']

    # Find unrated restaurants
    unrated_restaurants = [r for r in all_restaurants if r not in rated_restaurants.values]

    # Predict ratings for unrated restaurants
    predictions = [model.predict(user_id, restaurant) for restaurant in unrated_restaurants]
    predictions = sorted(predictions, key=lambda x: x.est, reverse=True)

    # Get top predictions
    top_predictions = predictions[:top_n]
    top_restaurants = [pred.iid for pred in top_predictions]

    # Fetch restaurant details
    return restaurants_data[restaurants_data['Restaurant'].isin(top_restaurants)]

global data_merged
def MergeDataset(request):
    global data_merged
    restaurants_data.rename(columns={'Name': 'Restaurant'}, inplace=True)
    data_merged=pd.merge(reviews_data, restaurants_data, on='Restaurant', how='inner')
    table = "<table  class='table'><thead  class='thead-dark'>"\
            "<tr><th scope='col'>Restaurant</th>" \
            "<th scope='col'>Review</th>" \
            "<th scope='col'>Rating</th>" \
            "<th scope='col'>Sentiment Score</th>" \
            "<th scope='col'>Collections</th>" \
            "<th scope='col'>Cuisines</th>" \
            "</tr></thead>"


    # Iterate over the rows of the DataFrame
    for _, row in data_merged.head(3).iterrows():
        table += f"""
                <tbody>
                <tr>
                <td>{row['Restaurant']}</td>
                <td>{row['Review']}</td>
                <td>{row['Rating']}</td>
                <td>{row['sentiment_score']}</td>
                <td>{row['Collections']}</td>
                <td>{row['Cuisines']}</td>
                </tr></tbody>
            """
        # Close the table
    table += "</table>"

    context={'data':table,'msg':'First Rename Name column in RestaurantName.csv column to Restaurant bcz Merging Two Datasets for context based filtering'}
    return render(request,'AdminApp/Merging.html',context)

# # Merge restaurant and review datasets
# def merge_datasets(restaurants_data, reviews_data):
#     restaurants_data.rename(columns={'Name': 'Restaurant'}, inplace=True)
#     return pd.merge(reviews_data, restaurants_data, on='Restaurant', how='inner')

def recommend_restaurants(food_item, user_id, restaurants_data, reviews_data, top_n=5):
    global data_merged
    # Preprocess data
    reviews_data = preprocess_ratings(reviews_data)
    # data_merged = merge_datasets(restaurants_data, reviews_data)

    # Train collaborative model if not already trained
    try:
        joblib.load("Model/svd_model.joblib")
    except FileNotFoundError:
        train_collaborative_model(reviews_data)

    # Get recommendations from both systems
    context_recommendations = recommend_context(food_item, data_merged, top_n)
    collaborative_recommendations = recommend_collaborative(user_id, reviews_data, restaurants_data, top_n)

    # Combine results (can use a weighting mechanism if desired)
    combined_recommendations = pd.concat([context_recommendations, collaborative_recommendations]).drop_duplicates(subset='Restaurant')
    return combined_recommendations




def Recommendation(request):
    return render(request,'AdminApp/Recommendation.html')

def RecommendAction(request):
    item_name=request.POST['food_item']
    userid=request.POST['userid']
    # Load datasets
    # restaurants_data = pd.read_csv("Datasets/Restaurant names.csv")
    # reviews_data = pd.read_csv("Datasets/Restaurant reviews.csv")
    # Recommend restaurants based on a food item
    top_recommendations = recommend_restaurants(item_name, userid, restaurants_data, reviews_data, top_n=5)
    # print(top_recommendations.columns)

    table = "<table  class='table'><thead  class='thead-dark'>" \
            "<tr><th scope='col'>Restaurant</th>" \
            "<th scope='col'>Links</th>" \
            "<th scope='col'>Cuisines</th>" \
            "<th scope='col'>Timings</th>" \
            "</tr>"


    # Iterate over the rows of the DataFrame
    for _, row in top_recommendations.head(5).iterrows():
            table += f"""
                    <tbody>
                    <tr>
                    <td>{row['Restaurant']}</td>
                    <td>{row['Links']}</td>                   
                    <td>{row['Cuisines']}</td>
                    <td>{row['Timings']}</td>
                    </tr><tbody>
                """
            # Close the table
    table += "</table>"


    context={'data':table}
    return render(request,'AdminApp/RecommendationResult.html',context)
def home(request):
    return render(request,'AdminApp/AdminHome.html')

def Customerlogin(request):
    return render(request,'AdminApp/ulogin.html')

def CustomerRegister(request):
    return render(request,'AdminApp/CustomerRegister.html')


@csrf_exempt
def CustomerRegisterAction(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if not (username and password and email and phone):
            return render(request, 'AdminApp/CustomerRegister.html', {
                "msg": "All fields are required.",
                "msg_tag": "danger"
            })

        # Check if username already exists in 'customer' table
        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM customer WHERE username = %s", [username])
        if cursor.fetchone():
            con.close()
            return render(request, 'AdminApp/CustomerRegister.html', {
                "msg": "Username already exists. Try a different one.",
                "msg_tag": "danger"
            })

        # Insert new user into 'customer' table
        cursor.execute("INSERT INTO customer (username, password, email, phone) VALUES (%s, %s, %s, %s)",
                       (username, password, email, phone))
        con.commit()
        con.close()

        return render(request, 'AdminApp/CustomerRegister.html', {
            "msg": "Registration successful! You can now login.",
            "msg_tag": "success"
        })

    return render(request, 'AdminApp/CustomerRegister.html')


from django.shortcuts import render, redirect
from AdminApp.Database import connection

def CustomerLoginAction(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        con = connection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM customer WHERE username=%s AND password=%s", [username, password])
        user = cursor.fetchone()
        con.close()

        if user:
            request.session['username'] = username
            return redirect('CustomerHome')  # Ensure this path exists in your urls.py
        else:
            return render(request, 'AdminApp/ulogin.html', {
                'msg': 'Invalid username or password',
                'msg_tag': 'danger'
            })

    return render(request, 'AdminApp/ulogin.html')


def CustomerHome(request):
    return render(request,'AdminApp/CustomerHome.html')  # or your login URL name



