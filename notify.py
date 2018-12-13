from urllib import request as ur
from bs4 import BeautifulSoup as bs
from twilio.rest import Client
from api_secrets import *
import json

client = Client(account_sid, auth_token)

def clean(l):
    for item in l:
        s = str(item)
        if s != "<br/>":
            if s.endswith(" V") or s.endswith(" *"):
                yield s[:-2]
            else:
                yield s

def get_chicken():
    content = ur.urlopen("https://www.haverford.edu/dining-services/dining-center").read()
    soup = bs(content,"lxml")
    todaymenu = soup.find("div",{"id":"today_menu_1"})
    meals = todaymenu.find_all("div",{"class","meal-container"})
    meals = [list(meal.p) for meal in meals]
    
    mealmenus = [set(list(clean(meal))) for meal in meals]
    mealnames = ["breakfast","lunch","dinner"]
    out = {"breakfast":[],"lunch":[],"dinner":[]}

    for menu, mealname in zip(mealmenus,mealnames):
            for food in menu:
                if food.lower() == "breaded chicken":
                    out[mealname].append("tendies")
                elif "oreo" in food.lower():
                    out[mealname].append(food.lower())
    return out

def sendmessage(message,number):
    print(number + ": " + message)
    message = client.messages.create(
        to=number, 
        from_="+12245058742",
        body=message)

x = get_chicken()
s = ""
for mealname, chickentypes in x.items():
    if len(chickentypes) != 0:
        s += "For %s there will be %s! " % (mealname, " and ".join(chickentypes))

with open("subs.json","r") as fh:
    subs = json.load(fh)

if s != "":
    for phone_number in subs:
        sendmessage(s,phone_number)
