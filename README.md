# RVK Calendar Newsletter

This is a showcase project intended to demonstrate some of the things you can do with the calender API.

This takes an email address and zero or more tags and sends you a weekly email of events that match.

You can also automatically deploy to Heroku by clicking the button
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

If you deploy this to Heroku, you will need to go to the Scheduler Add-On and set the time when you want this reminder to be sent. For the command you will use the same as if you were running this locally:

python send.py

To run this locally you can type. Before this, it will be looking for several local environmental variables. To set these type:

export TO_EMAIL=youremail@example.com
export MANDRILL_USERNAME=Your-mandrill-username
export MANDRILL_APIKEY=Your-API-KEY
export CATEGORIES=comma,separated,list,of,keywords

python send.py

This will fetch the event from the API and send you an email based on mandrill SMTP credientials