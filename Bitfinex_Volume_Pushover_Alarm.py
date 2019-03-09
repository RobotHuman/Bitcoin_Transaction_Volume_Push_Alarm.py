import time
import datetime
import urllib, urllib2
import httplib
import simplejson
transactions_clipped = []
last_push_time = 0


period = 1200 # in seconds
volume_threshold = 1500 #transaction volume threshold.  Any time this is exceeded, you will get a push notification.

Pushover_on = True #we can turn push notifications on or off
push_interval = 600
sound_number = 6

def SimpleJason(url): #Jason, such a simple man
	req = urllib2.Request(url)
	opener = urllib2.build_opener()
	f = opener.open(req, timeout = 10)
	return simplejson.load(f)

def Transactions():
	try:
		data = SimpleJason("https://api.bitfinex.com/v1/trades/btcusd")
	except Exception, e:
		print e
		data = []
	return data
	
def getVolume(data, period):
	#Returns transaction volume in a given data set
	#from 0 to 'period' seconds ago
	time_threshold = data[0]['timestamp']-period
	filtered = []
	volume = 0
	for x in data:
		if x['timestamp'] > time_threshold:
			filtered = filtered + [x]
			volume = volume + float(x['amount'])

	return filtered, volume
	
def Pushit(message, sound):
	#interfaces with Pushover API
	#sends a message and a sound
	
	print "pushing sound " + str(sound) + " and message " + message
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
	urllib.urlencode({
		"token": "YOUR TOKEN HER",
		"user": "YOUR USER TOKEN HER",
		"message": message,
		"sound": sound,
		}), { "Content-type": "application/x-www-form-urlencoded" })
	conn.getresponse()

	
def PushSound(message, sound):
	#pushes out a notification with a sound
	
	
	if(sound == 0):
		Pushit(message, "cashregister")
	elif(sound == 1):
		Pushit(message, "falling")
	elif(sound == 2):
		Pushit(message, "incoming")
	elif(sound == 3):
		Pushit(message, "cosmic")
	elif(sound == 4):
		Pushit(message, "tugboat")
	elif(sound == 5):
		Pushit(message, "bike")
	elif(sound == 6):
		Pushit(message, "bugle")
	elif(sound == 7):
		Pushit(message, "classical")
	elif(sound == 8):
		Pushit(message, "gamelan")
	elif(sound == 9):
		Pushit(message, "intermission")
	elif(sound == 10):
		Pushit(message, "mechanical")
	elif(sound == 11):
		Pushit(message, "pianobar")
	elif(sound == 12):
		Pushit(message, "siren")
	elif(sound == 13):
		Pushit(message, "spacealarm")
	elif(sound == 14):
		Pushit(message, "alien")
	elif(sound == 15):
		Pushit(message, "climb")
	elif(sound == 16):
		Pushit(message, "persistent")
	elif(sound == 17):
		Pushit(message, "echo")
	elif(sound == 18):
		Pushit(message, "updown")
	elif(sound == 19):
		Pushit(message, "magic")
	elif(sound == 20):
		Pushit(message, "pushover")
	else:
		Push(message + " mistyped sound")
		print "mistyped sound", sound
	
while(True):	
	trans = Transactions() + transactions_clipped
	if len(trans)>0: 
		trans = [i for n, i in enumerate(trans) if i not in trans[n + 1:]] 
		
	if len(trans)>0:
		transactions_clipped, volume = getVolume(trans, period)
		print(volume)
		if volume > volume_threshold:
			if(Pushover_on and time.time() - last_push_time > push_interval):
				last_push_time = time.time()
				PushSound('volume threshold reached! ' + str(volume) + ' bitcoins traded in the past ' + str(period) + ' seconds!', sound_number)
	time.sleep(5)
