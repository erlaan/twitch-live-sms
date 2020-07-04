# Prerequisite
You need Twitchclient and twilio
## Installation instruction with pip
pip3 install python-twitch-client
pip3 install twilio

# Running the Program
Fill the variable.env with all the neassary information. When done type source ./variable.env

Or just run this command in the terminal
* export TWILIO_ACCOUNT_SID=''
* export TWILIO_AUTH_TOKEN=''
* export API_KEY=''
* export MYPHONENUMBER=''
* export TWILIO_PHONENUMBER=''

Then you need to go in to twithc-live-sms.py and change channel variable to the channelname you want a notification for. 

Then just do python3 twitch-live.sms.py


# Todo 
- [ ] Channel Selection on command line
- [ ] Bugfixing?
- [ ] Fix bug that it disconnect random. 

