from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import json

application = Flask(__name__)

@application.route("/")
def hello():
    return "<h1 style='color:blue'>Welcome to Haverford Tendies Alerts!</h1>"

@application.route("/sms", methods=["POST"])
def sms_reply():
    body = request.values.get('Body', None).lower().strip()
    sender = request.values.get('From',None)
    resp = MessagingResponse()
    with open("subs.json","r") as fh:
        subs = json.load(fh)

    if body == "i luv tendies":
        if sender in subs:
            resp.message("You are already subscribed to Haverford Tendies Alerts.")
        else:
            subs.append(sender)
            resp.message("Thanks! You are now registered for Haverford Tendies Alerts! Text \"i h8 tendies\" at any time to cancel!")
    elif body == "i h8 tendies":
        if sender in subs:
            subs.remove(sender)
            resp.message("You have been successfully unsubscribed from Haverford Tendies Alerts!")
        else:
            resp.message("You are not subscribed to Haverford Tendies Alerts.")
    elif body == "subs":
        if sender == "+18287850136":
            resp.message(str(subs))
        else:
            resp.message("You are not authorized to receive that information.")
    else:
        resp.message("Hi! This is Haverford Tendies Alerts! Please text \"i luv tendies\" to subscribe or \"i h8 tendies\" to unsubscribe.")
    
    with open("subs.json","w") as fh:
        json.dump(subs,fh)
    return str(resp)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
