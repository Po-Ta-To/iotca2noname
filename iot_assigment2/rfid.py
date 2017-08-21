import RPi.GPIO as GPIO
import MFRC522
import signal
import datetime

from dbconnect import connection
from gpiozero import LED, Button
from signal import pause

import sys 
import Adafruit_DHT
from time import sleep

led1 = LED(18)
led2 = LED(23)

led_state = True;

uid = None
prev_uid = None
continue_reading = True
data=[]


#get card number from database and put it as array/list
def getCard():
	global data
	print("connect to database...")
	
	try:
		c, conn = connection()
		
		query = "select cardId, userId from account"
		c.execute(query);
		rows = c.fetchall()
		
		for row in rows:
			
			cardId = str(row[0])
			userId = str(row[1])
			
			#json = {'cardId':cardId, 'userId':userId}
			data.append(cardId)
			print(cardId + " from get card")
		
		print("done getting data, disconnect from database...")
		c.close();
		conn.close();
			
		#return data
	except Exception as e:
		#return(str(e))
		print(str(e))

		
		
def addLog(cardId):
	classId = "classroom_zw"
	print("connect to database...")
	
	try:
		c, conn = connection()
		
		#query = "insert into cardAccessLog (cardId,classId,logDateTime) values (?,?)",(cardId,classId,datetime.datetime.now())
		c.execute("insert into cardAccessLog (cardId,classId) values (%s,%s)",(cardId,classId))
		conn.commit()

		print("added data, disconnect from database...")
		c.close();
		conn.close();
	except Exception as e:
		#return(str(e))
		print(str(e))
getCard()

#led on and off
def led1ON():
	led1.on()
	print("LED 1 is on")

def led1OFF():
	led1.off()
	print("LED 1 is OFF")

def led2ON():
	led2.on()
	print("LED 2 is on")

def led2OFF():
	led2.off()
	print("LED 2 is OFF")

#toggle led
def toggle_led():
	global led_state
	if led_state == True:
		led1ON()
		led2ON()
		led_state = False
	else:
		led1OFF()
		led2OFF()
		led_state = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	global continue_reading
	print "Ctrl+C captured, ending read."
	continue_reading = False
	GPIO.cleanup()
	
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
mfrc522 = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips.
# If one is near it will get the UID

while continue_reading:

	#Get humidity
	'''
	humidity, temperature = Adafruit_DHT.read_retry(11, 4)
	print('temp: {:.1f} C'.format(temperature))
	print('humidity: {:.1f}'.format(humidity))
	'''
	# Scan for cards
	(status,TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)
	
	# If a card is found
	if status == mfrc522.MI_OK:
		# Get the UID of the card
		(status,uid) = mfrc522.MFRC522_Anticoll()
		#if uid!=prev_uid:
		#	prev_uid = uid
		print("New card detected! UID of card is {}".format(uid)) 
		tempuid = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+","+str(uid[4])
		
		
		
		#getCard()
		for row in data:
			print(row)
			if tempuid == row:
				print('on led')
				toggle_led()
			else:
				print('cannot')
				
		#add cardid to log
		addLog(tempuid)
		
	sleep(1)