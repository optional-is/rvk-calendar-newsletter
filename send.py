#coding:utf-8
import os
import sys
import csv
import json
import requests
from smtplib import SMTP
import datetime

if __name__ == "__main__":
	# Look at the enviornmental variables to check for a receipient email and any categories to filter by
	if os.environ.get('TO_EMAIL',False):
		categories = os.environ.get('CATEGORIES',False)
		lang       = os.environ.get('LANGUAGE','en')
		
		# Fetch RVK Event JSON Data
		# CURL Request to the JSON endpoint. Pass the language, any category filters and today's date+7 days
		json_data = json.decode('{}')
		
		# Put the data and the template together
		message_text = ''
		
		# send the message
		smtp = SMTP()
        smtp.connect('smtp.mandrillapp.com', 587)
        smtp.login(os.environ.get('MANDRILL_USERNAME'), os.environ.get('MANDRILL_APIKEY'))
    
        from_addr = "RVK Calendar <calendar@example.com>"
        to_addr = [os.environ.get('TO_EMAIL')]
    
		# Put this into a template or something to localize it easier
        subj = "X new events this week"

        date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
    
        msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s"  % ( from_addr, ', '.join(to_addr), subj, date, message_text )
    
        smtp.sendmail(from_addr, to_addr, msg)
        smtp.quit()