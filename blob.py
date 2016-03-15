#!/usr/bin/python
import sys, time, random
#from pygame.locals import *
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()
sense.low_light = True
#pygame.init()
#pygame.display.set_mode((1,1))

blob = {
        'x' : 4,
        'y' : 3
}
food_pos = {
	'x' :  4,
	'y' : 5 
}
move = {
	'left' : False,
	'right' : False,
	'up' :  False,
	'down' : False
}
sleeping = False
detect_movement = False
walk_frequency = 200
food_visible = False
hunting = False
scared = False


blue = [0,0,255]
red = [255,0,0]
orange = [210,120,0]
white = [255,255,255]
purple = [255,0,255]
green = [0,75,0]

color = blue

sense.set_rotation(180)

def get_accelerometer_sleep():
        global detect_movement, blob
        x,y,z = sense.get_accelerometer_raw().values()
        x = abs(x)
        y = abs(y)
        z = abs(z)
        #print x,y,z
        if x > 1 or y > 1 or z > 1:
                detect_movement = True
                print "Detect_movement: " + str(detect_movement)
        else:
                detect_movement = False
        return detect_movement

def get_accelerometer_awake():
        global blob
        x,y,z = sense.get_accelerometer_raw().values()
        x = round(x,0)
        y = round(y,0)
        z = round(z,0)
        if y < 0:
                sense.clear()
                blob['x'] += 1
        if y > 0:
                sense.clear()
                blob['x'] -= 1
        if x < 0:
                sense.clear()
                blob['y'] += 1
        if x > 0:
                sense.clear()
                blob['y'] -= 1
       # return detect_movement

def proximity_sensor_intit():
        global humidity_baseline, humidity, proximity_delay_tick, sum_humidity
        humidity_baseline = round(sense.get_humidity(), 1)
        humidity =[ 1,2,3,4,5,6,7,8,9]
        proximity_delay_tick = 0
        sum_humidity = 0
        
        
def proximity_calc():
        global clock_tick, humidity_baseline, humidity, \
        sum_humidity, proximity_delay_tick, proximity_detected, color, scared

        if clock_tick - 1 > proximity_delay_tick:
                i = proximity_delay_tick
                if i > 8:
                        i = 0
                        proximity_delay_tick = 0
                humidity[i] = round(sense.get_humidity(), 1)
               # print humidity[i]

                proximity_delay_tick += 1
                clock_tick = 0
                #print proximity_delay_tick
        
        for i in range(0,9):
                sum_humidity = humidity[i] + sum_humidity

        mean = sum_humidity / 9
        #print mean
        if humidity_baseline > round((mean + 3), 1):
                humidity_baseline = round(sense.get_humidity(), 1)
        elif humidity_baseline < round((mean - 3), 1):
                humidity_baseline = round(sense.get_humidity(), 1)
       # print humidity_baseline,  round(sense.get_humidity(), 1)

        if round(sense.get_humidity(), 1) > humidity_baseline + 1.5:
                proximity_detected = True                
        else:
		scared = False
                proximity_detected = False
                color = blue
        #print proximity_detected
        mean = 0
        sum_humidity = 0
        return proximity_detected

def main_ai_loop():
        global scared, sleeping, proximity, walk_frequency, proximity, color, detect_movement, hunting
        rn = random.randrange(0, 1300)
        
        if sleeping == True:
                sleeping = sleep_ai()
        else:
                proximity = proximity_calc()
                if proximity == True:
                        color = orange
                        walk_frequency = 1300
                        hunting = False
			if scared == False:
				print "Got Scared! True"
				scared = True

                else:
                        walk_frequency = 200
                if rn < walk_frequency:
                        move_decision = True
                        blob_move_ai()
                elif rn == 998 and proximity == False:
                        sleeping = True
                        print "Sleeping: " + str(sleeping)
                ##cleanup:
                move_decision = False
                get_accelerometer_awake()
def sleep_ai():
        global sleeping, color, detect_movement
        color = purple
        rn = random.randrange(0,1100)
        detect_movement = get_accelerometer_sleep()
        if rn == 30:
                color = blue
                sleeping = False
                print "Sleeping: " + str(sleeping)
        elif detect_movement == True:
                color = blue
                sleeping = False
                print "Sleeping: " + str(sleeping)
        else:
                sleeping = True
                #print rn
        time.sleep(0.1)
        return sleeping
def blob_move_ai():
        global blob, decision, move
        rn = random.randrange(0,100)
        if hunting == True:
        	if rn < 50:
        		if move['left'] == True:
        	        	draw()
        	       		blob['x'] -= 1
        	       	elif move['right'] == True:
        	       		draw()
        	       		blob['x'] += 1
        	       	elif move['up'] == True:
        	       		draw()
        	       		blob['y'] -= 1
        	       	elif move['down'] == True:
	       			draw()
	       			blob['y'] += 1
	       	for _ in move:
	       		move[_] = False
	else: 
		if rn < 10:
		        draw()
		        blob['x'] += 1
		elif rn < 20 and rn > 10:
		        draw()
		        blob['x'] -= 1
		elif rn > 30 and rn < 40:
		        draw()
		        blob['y'] += 1
		elif rn > 50 and rn < 60:
		        draw()
		        blob['y'] -= 1
                
def draw():
	sense.clear()
	if food_visible == True:
		food()

def blob_terrarium_collision():
        global blob
        if blob['x'] >= 7:
                blob['x'] = 7
                if blob['y'] >= 7:
                        blob['y'] = 7
                if blob['y'] <= 0:
                        blob['y'] = 0
                sense.set_pixel(blob['x'],blob['y'],white)
                #time.sleep(0.05)
        if blob['x'] <= 0:
                blob['x'] = 0
                if blob['y'] >= 7 :
                        blob['y'] = 7
                if blob['y'] <= 0:
                        blob['y'] = 0
                sense.set_pixel(blob['x'],blob['y'],white)
                #time.sleep(0.05)
        if blob['y']  >= 7:
                blob['y'] = 7
                
                sense.set_pixel(blob['x'],blob['y'],white)
                #time.sleep(0.05)
        if blob['y'] <= 0:
                blob['y'] = 0
                sense.set_pixel(blob['x'],blob['y'],white)
                #time.sleep(0.05)
                
def food():
	global food_pos, food_visible
	sense.set_pixel(food_pos['x'],food_pos['y'],green)
	if blob['x'] == food_pos['x'] and blob['y'] == food_pos['y']:
		food_visible = False
		print "Food Eaten"
def spawn_food():
                global food_pos, food_visible
                rnX = random.randrange(0,7)
                rnY = random.randrange(0,7)
                food_pos['x'], food_pos['y'] = rnX, rnY
                food_visible = True
def food_hunting_ai():
	global blob, hunting
	rn = random.randrange(0, 500)
	if blob['x'] > food_pos['x'] and blob ['x'] <= food_pos['x'] + 3:
		hunting = True
		move['left'] = True
	elif blob['x'] < food_pos['x'] and blob ['x'] >= food_pos['x'] - 3:
		hunting = True
		move['right'] = True
	elif blob['y'] > food_pos['y'] and blob['y'] <= food_pos['y'] + 3:
		hunting = True
		move['up'] = True
	elif blob['y'] < food_pos['y'] and blob['y'] >= food_pos['y'] - 3:
		hunting = True
		move['down'] = True
	else:
		hunting = False
def world_events_loop():
	god = random.randrange(0,1100)
	if god == 33 and food_visible == False:
		spawn_food()
		print "Food Spawned"
	
###intit###
proximity_sensor_intit()
clock_tick = 0
#spawn_food()
while True:
        clock_tick += 1
        world_events_loop()
        main_ai_loop()
        blob_terrarium_collision()
        if food_visible == True:
	       food()
	       food_hunting_ai()
        sense.set_pixel(blob['x'],blob['y'],color)
        
        time.sleep(0.2)
