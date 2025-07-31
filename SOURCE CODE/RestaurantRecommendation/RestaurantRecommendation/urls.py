"""RestaurantRecommendation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AdminApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name='index'),
    path('AlogAction', views.AlogAction),
    path('home', views.home),
    path('Upload', views.Upload),
    path('UploadAction', views.UploadAction),
    path('predatasets', views.predatasets),
    path('MergeDataset', views.MergeDataset),
    path('SentimentScore',views.SentimentScore),
    path('Recommendation', views.Recommendation ,name='Recommendation'),
    path('RecommendAction', views.RecommendAction),
    path('Customerlogin', views.CustomerLoginAction, name='Customerlogin'),
    path('CustomerLoginAction', views.CustomerLoginAction, name='CustomerLoginAction'),
    path('CustomerRegister', views.CustomerRegister, name='CustomerRegister'),
    path('CustomerRegisterAction', views.CustomerRegisterAction, name='CustomerRegisterAction'),
    path('CustomerHome', views.CustomerHome, name='CustomerHome'),
]



