from twitch import TwitchClient
from twilio.rest import Client
import os
import time
import datetime
import sys


#Variables
channels=["twitchchannel","twitchchannel2"]
api_key= os.environ['API_KEY']  #It getting the API_KEY from OS so make sure to do export API_KEY='XXXXXXXXXXXXXXXXXXXXX'
livestatus={}            #This make sure we do not spam SMS to the Reciver
t0={}                 #This is used to calculate the live time for the streamer
smsclient = Client(os.environ['TWILIO_ACCOUNT_SID'],os.environ['TWILIO_AUTH_TOKEN']) #It getting the SID and Token from OS so make sure to run export TWILIO_ACCOUNT_SID='XXXXXXXXXXXXXXXXXXXXX' and export TWILIO_AUTH_TOKEN='XXXXXXXXXXXXXXXXXXXXX'
phonenumber= os.environ['MYPHONENUMBER'] #Do export MYPHONENUMBER="+46XXXXXXXXX"
print(sys.argv)
try:    # This will test if the user have input a file as a argument other wise it will go for the channels defiend above.
    with open(sys.argv[1]) as f:
        channels=f.read().splitlines()
except IndexError:
    pass  #No files defiend as a sys.argv going with the channels

for channel in channels:
    livestatus[channel]=0
    t0[channel]=0

twitchclient = TwitchClient(client_id=api_key)

def getid(twitchclient,channel):
    users = twitchclient.users.translate_usernames_to_ids(channel)
    for user in users:
        user_id='{}'.format(user.id)
    return user_id
def live(twitchclient,channelid,smsclient, phonenumber,channel):
    global livestatus
    global t0
    live=twitchclient.streams.get_stream_by_user(channelid)
    if(live==None):
        if(livestatus[channel]==0):
            print(channel+" is offline")
            livestatus[channel]=0
        elif(livestatus[channel]==1):
            print("OFFLINE: SENDING SMS")
            t1=time.time()
            totaltime = t1-t0[channel]
            hours = int(totaltime/3600)
            minutes = int((totaltime%3600)/60)
            seconds = int((totaltime%60))
            livestatus[channel]=0
            sms(smsclient, phonenumber,"Now "+channel+" is OFFLINE Was live for "+str(hours)+"h "+str(minutes)+"m "+str(seconds)+"s")
            time.sleep(30) #This sleep is for the bug that the seems to go live and offline. For some seconds
    else:
        live_broadcast=live['broadcast_platform']
        if(livestatus[channel]==1):
            print(channel+" is LIVE")
        elif(live_broadcast=="rerun"):
            print("it'is a rerun do nothig")
        elif(live_broadcast=="live"):
            print(channel+" is LIVE: Sending SMS")
            t0[channel]=time.time()
            livestatus[channel]=1
            sms(smsclient, phonenumber,"Now is the "+channel+" LIVE! Go and watch at https://twitch.tv/"+channel)

def sms(smsclient,phonenumber,msg):
    smsclient.messages \
                .create(
                     body=msg,
                     from_=os.environ['TWILIO_PHONENUMBER'],
                     to=phonenumber
                 )


while True:
    try:
        for channel in channels:
            live(twitchclient,getid(twitchclient,channel),smsclient,phonenumber,channel)
    except KeyboardInterrupt:
        break
    except:
        continue