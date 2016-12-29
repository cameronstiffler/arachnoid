#Robot Leg Animation Engine Developed by cameronstiffler@gmail.com 2016


import os
import time
from collections import deque

os.system('sudo ./servod --p1pins 13,11,7,15,12,16,18,22 --p5pins 3,5,4,6')

delay = .005
CALIBRATEPOS = [[[50,1],[50,1],[50,1]]]

def reverse(num):
	return 100-num

#----Class Definitions-----

class Servo:
	def __init__(self,id,pin,startingPosition,isReversed,min,max):
		self.id = id
		self.pin = pin
		self.reversed = isReversed
		self.rate = 1.8
		self.offset = 0
		self.min = min
		self.max = max
		self.moveQueue = deque([50])
		self.end = 0		
		self.position = 0
		#os.system("echo "+self.pin+"="+self.position+" > /dev/servoblaster") //not longer using servo blaster
		#debug()
		#print "created servo "+str(self.id)
	
	def setPosition (self,end):
		if self.reversed:
			self.end = reverse(end)
		else:
			self.end = end
		#print "setting physical position of servo "+str(self.id)+" to "+str(self.end)
	
	def getPosition (self):
                if self.reversed:
                        return reverse(self.position)
                else:
                        return self.position

	def addToQueue (self,q):
		for i in q:
			#print str(i)
			if self.reversed:
				self.moveQueue.append(reverse(i))
			else:
				self.moveQueue.append(i)
				
	def setQueue (self,q):
		for i in q:
			if self.reversed:
				self.moveQueue[0] = reverse(i)
			else:
				self.moveQueue[0] = i
				
	def setQueueRate (self,q):
		for i in q:
			if self.reversed:
				self.moveQueue[0] = reverse(q[0])
			else:
				self.moveQueue[0] = q[0]
			if len(q)==2:
				self.rate = q[1]
				
	def setOffset (self,off):#is not wired in to update
                if self.reversed:
                        self.offset = reverse(off)
                else:
                        self.offset = off

	def update(self):
		if (self.moveQueue):
			self.end = self.moveQueue[0]
			if self.position != self.end:
				self.move()
			else:
				self.moveQueue.popleft()
		
			

	def debug(self):
		#pass
		print "servo:"+str(self.id)+" position:"+str(self.position)+" end: "+str(self.end)+" rate:"+str(self.rate)+" pin:"+str(self.pin)+" offset:"+str(self.offset)+" reversed:"+str(self.reversed)
			
	def move(self):
		if ((self.position > self.end) and (self.position - self.rate >= self.end)): 
			#print "end < position"
			self.position = self.position - self.rate
			os.system("echo "+str(self.pin)+"="+str(self.position)+"% > /dev/servoblaster")
		elif ((self.position < self.end) and (self.position +self.rate <= self.end)): 
                        self.position = self.position + self.rate
			#print "end > position"
			os.system("echo "+str(self.pin)+"="+str(self.position)+"% > /dev/servoblaster")
		elif ((self.position < self.end) and (self.position + self.rate > self.end)):
                        self.position = self.end
			os.system("echo "+str(self.pin)+"="+str(self.position)+"% > /dev/servoblaster")
		elif ((self.position > self.end) and (self.position - self.rate < self.end)):
			self.position = self.end
			os.system("echo "+str(self.pin)+"="+str(self.position)+"% > /dev/servoblaster")
		self.debug()
		
	def clear(self):
		self.moveQueue = deque([])


class Leg:
	def __init__(self,id,servo0,servo1,servo2):
		self.id = id
		self.currentPosition = 0
		self.servos = servo0,servo1,servo2
	        self.moveQueue = deque([])
		 #print "created leg "+str(self.id)+" with "+str(self.servos)
    
	def update(self):
		allPointsReached = True#as far as we know
		sCount = 0
		if (self.moveQueue):
			for p in self.moveQueue[0]:	
				#self.servos[sCount].addToQueue([p])
				#self.servos[sCount].setQueueRate([p])
				self.servos[sCount].setQueueRate(p)#assumes a list is handed
           			if self.servos[sCount].getPosition() != p[0]:
                			allPointsReached = False#so dont move to next position set
                			self.servos[sCount].update()
            			sCount = sCount + 1
	        	if allPointsReached:
        	    		self.moveQueue.popleft()
                    
	def addToQueue(self,q):
		q = self.optomizeSegment(q,1)
		for i in q:
            		positionSet = []#holder for new and parsed position set
            		pCount = 0
            		for p in i:#iterate through values in position set
                    		if self.servos[pCount].reversed:
					positionSet.append(p)
                    		else:
					positionSet.append(p)
        		self.moveQueue.append(positionSet)
    
	def getCurrentPosition(self):
		position = []
	    	for s in self.servos:
    			position.append([s.position])
    		return position
    		
    	
	def optomizeSegment(self,m,multiplier): #format: [[[a1],[b1],[c1]],[[a2],[b2],[c2]],[[a3],[b3],[c3]]] multiplier = 1 or 1.2 or .8 as examples
    		count = 0
    		result = []
    		for i in m:
    			if count > 0:
				print "m count -1"
    				optomizedi = self.optomizeMovement(i,m[count-1],multiplier)
    			else:	
				print "m count doesnt exist"+str(self.getCurrentPosition())
    				optomizedi = self.optomizeMovement(i,self.getCurrentPosition(),multiplier)
    			result.append(optomizedi)
    			count = count +1
    		print "optomizeSegment Result: "+str(result)
    		return result
    	
	def optomizeMovement(self,p1,p2,multiplier): #format: [[a1],[b1],[c1]],[[a2],[b2],[c2]],
		print "optomizeMovement recieved: "+str(p1)+" and "+str(p2)
    		count = 0
    		shortestDistance = self.getShortestMove(p1,p2)
    		result = []
    		for i in p1:
			step = 1
    			j = p2[count]
    			p1Distance = i[0]
    			p2Distance = j[0]
    			if ((abs(p1Distance-p2Distance) > shortestDistance) and (abs(p1Distance-p2Distance) !=shortestDistance -1)):
				if ((abs(p1Distance-p2Distance) != 0) and (abs(p1Distance-p2Distance) != shortestDistance)):
    					step = abs(p1Distance-p2Distance)/shortestDistance
				else:
					step = 1
    			elif (abs(p1Distance-p2Distance)+1 == shortestDistance-1):
    				step = 1
			
    			iList = [0,0]
    			iList[0]=i[0]
    			iList[1]=step
    			result.append(iList)
    			count = count +1
    		return result
    	
	def getLongestMove(self,p1,p2):
    		count = 0
    		longestDistance = -1
    		for i in p1:
    			j = p2[count]
    			p1Distance = i[0]
    			p2Distance = j[0]
    			if abs(p1Distance-p2Distance) > longestDistance:
    				longestDistance = p1Distance
    		return longestDistance
    		
    	def getShortestMove(self,p1,p2):
    		count = 0
    		shortestDistance = 10000
    		for i in p1:
    			j = p2[count]
    			p1Distance = i[0]
    			p2Distance = j[0]
    			if ((abs(p1Distance-p2Distance) < shortestDistance) and (abs(p1Distance-p2Distance) != 0)):
    				shortestDistance = abs(p1Distance-p2Distance)
		if ((shortestDistance == 10000) or (shortestDistance == 0)):
			return 1
		else:
    			return shortestDistance
    	
	def clear(self):
		self.moveQueue = deque([])
		for s in self.servos:
			s.clear()
		
class Bot:
	def __init__(self,id,legs):
		self.id = id
		self.currentPosition = [0,0]
		self.legs = legs
	    	self.moveQueue = deque([])#enter x and y -[[x,y]] and it just moves there
    
	def update(self):
		for l in legs:
			l.update()
			
	def clear(self):
		self.moveQueue = deque([])
		for l in legs:
			l.clear()
			
	def walkTo(self,x,y,rate):
		pass #add walk functionality
		
	def calibrate(self,CALIBRATEPOS):
		self.clear()
		for l in legs:
			l.clear()
			l.addToQueue(CALIBRATEPOS)
#----End Class Definitions----


#initialize servos and legs they belong to. Servo data: id,pin,startingPosition,servo is Reversed. servos will be normal on one side and reversed on other side of bot ,min,max.
#Leg data: id,servos...

s0 = Servo(0,0,51,False,0,50)
s1 = Servo(1,1,21,True,0,50)
s2 = Servo(2,2,41,False,0,50)
legR1 = Leg(0,s0,s1,s2)

s3 = Servo(3,3,1,True,0,50)
s4 = Servo(4,4,21,False,0,50)
s5 = Servo(5,5,41,True,0,50)
legL1 = Leg(7,s3,s4,s5)

s6 = Servo(6,6,51,False,0,50)
s7 = Servo(7,7,21,True,0,50)
s8 = Servo(8,8,51,False,0,50)
legR2 = Leg(3,s6,s7,s8)

s9 = Servo(9,9,51,True,0,50)
s10 = Servo(10,10,21,False,0,50)
s11 = Servo(11,11,51,True,0,50)
legL2 = Leg(4,s9,s10,s11)

legs = legR1,legL1,legR2,legL2

#initialize bot instance and assign legs to it
bot = Bot(0,legs)

#Adding to leg queue example. All servos must be in position before next position set is loaded into queue  


#------Position Matrices------
stand = [[55,20,40]]
standRate = [[[55],[20],[45]]]
standRateBack = [[[50],[20],[60]]]

testSegment = [[[0],[0],[20]],[[0],[20],[60]],[[20],[40],[0]],[[0],[0],[20]],[[0],[20],[60]]]

#Leg movement example. 3 servos in leg will move from one position to the next all coming to reset at the same time
legs[1].addToQueue(testSegment)

#Adding to servo queue example. Servo will move independantly of others.
#legs[0].servos[0].addToQueue([0,90,45])

#impliment queue for a leg to synch them all... give legs points with 3 positions example: (30,45,50),(20,40,65)

#main loop
while True:
	bot.update()
	time.sleep(delay)




