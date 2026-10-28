from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class expert(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    post = models.CharField(max_length=100)
    pin=models.CharField(max_length=20)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)

    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)

class farmer(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    pin=models.CharField(max_length=20)
    post=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    latitude=models.CharField(max_length=200)
    longitude=models.CharField(max_length=200)
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)

class tips(models.Model):
    tips=models.CharField(max_length=600)
    date=models.CharField(max_length=30)
    EXPERT = models.ForeignKey(expert, on_delete=models.CASCADE)
class complaint(models.Model):
    complaint=models.CharField(max_length=1000)
    complaint_date=models.CharField(max_length=30)
    reply=models.CharField(max_length=1000)
    reply_date=models.CharField(max_length=30)
    FARMER = models.ForeignKey(farmer, on_delete=models.CASCADE)
class farming_news(models.Model):
    news=models.CharField(max_length=1000)
    news_date=models.CharField(max_length=30)
    EXPERT= models.ForeignKey(expert, on_delete=models.CASCADE)
class marketing_prices(models.Model):
    crops=models.CharField(max_length=100)
    prices=models.CharField(max_length=1000)
    date = models.CharField(max_length=30)
    EXPERT = models.ForeignKey(expert, on_delete=models.CASCADE)
class subsidy(models.Model):
    subsidy_details=models.CharField(max_length=1000)
    subsidy=models.CharField(max_length=1000)
    subsidy_fromdate=models.CharField(max_length=30)
    subsidy_todate=models.CharField(max_length=30)
    EXPERT= models.ForeignKey(expert, on_delete=models.CASCADE)
class schmes(models.Model):
    schme_info=models.CharField(max_length=1000)
    EXPERT = models.ForeignKey(expert, on_delete=models.CASCADE)
    date=models.CharField(max_length=30)
    file = models.CharField(max_length=10000)


class chat(models.Model):
    message=models.CharField(max_length=1000)
    date=models.CharField(max_length=30)
    Expert = models.ForeignKey(expert, on_delete=models.CASCADE)
    FARMER = models.ForeignKey(farmer, on_delete=models.CASCADE)
    type= models.CharField(max_length=30)

class chatbot(models.Model):
    message=models.CharField(max_length=5000)
    date=models.CharField(max_length=30)
    FARMER = models.ForeignKey(farmer, on_delete=models.CASCADE)
    type= models.CharField(max_length=30)


