#coding: utf-8
import os
import sys
import csv
import json
from smtplib import SMTP
from cStringIO import StringIO
from email.mime.multipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.header import Header
from email import Charset
from email.generator import Generator
import datetime
import urllib2
	
if __name__ == "__main__":
	# Look at the enviornmental variables to check for a receipient email and any categories to filter by
	if os.environ.get('TO_EMAIL',False):
		categories = os.environ.get('CATEGORIES',False)
		if categories:
			categories = categories.split(',')
		else:
			categories = []
			
		lang       = os.environ.get('LANGUAGE','en')
		
		# Fetch RVK Event JSON Data
		# CURL Request to the JSON endpoint. Pass the language, any category filters and today's date+7 days
		# Fetch the JSON
		start = datetime.datetime.today().strftime("%Y-%m-%d")
		end = (datetime.datetime.today()+datetime.timedelta(days=7)).strftime("%Y-%m-%d")
		
		url="http://newevents.reykjavik.is/find?start__gte=%s&end__lte=%s&lang=%s"%(start,end,lang)
		
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		events = json.loads(response.read())
				
		# Put the data and the template together
		message_text = u''
		event_counter = 0

		for i in events:
			show = False

			for j in i['language']['en']['tags']:
				if j in categories:
					show = True

			if show or len(categories) == 0:
				message_text += u''+i['language']['en']['title']+"\n"
				message_text += u''+i['start']+' - '+i['end']+"\n"
				message_text += u''+i['language']['en']['text']+"\n"
				message_text += "\n\n"
				event_counter += 1
				
				
		# send the message
		smtp = SMTP()
		smtp.connect('smtp.mandrillapp.com', 587)
		smtp.login(os.environ.get('MANDRILL_USERNAME'), os.environ.get('MANDRILL_APIKEY'))
		
		from_addr = "RVK Calendar <calendar@example.com>"
		to_addr = [os.environ.get('TO_EMAIL')]
		
		# Put this into a template or something to localize it easier
		subj = u"%s new events this week"%event_counter
		
		date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )
		
		Charset.add_charset('utf-8', Charset.QP, Charset.QP, 'utf-8')
		msg = MIMEMultipart("alternative")
		
		msg['From'] = Header(from_addr.encode('utf-8'), 'UTF-8').encode()
		msg['To'] = Header(', '.join(to_addr).encode('utf-8'), 'UTF-8').encode()
		msg['Subject'] = Header(subj.encode('utf-8'), 'UTF-8').encode()
		
		msg.attach(MIMEText(message_text.encode('utf-8'),'plain','utf-8'))
		#msg.attach(MIMEText(message_text.encode('utf-8'),'html','utf-8'))
		
		io = StringIO()
		g = Generator(io, False) # second argument means "should I mangle From?"
		g.flatten(msg)

		# For Degubbing
		#print io.getvalue()
		
		# send the message!
        smtp.sendmail(from_addr, to_addr, io.getvalue())
        smtp.quit()

	
	