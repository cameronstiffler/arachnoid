#!/usr/bin/python

import time
import datetime
from Adafruit_8x8 import EightByEight
import cv

# ===========================================================================
# 8x8 Pixel Example
# ===========================================================================
rightEye = EightByEight(address=0x70,debug=True)
leftEye = EightByEight(address=0x71,debug=True)
defaultBright = 2



print "Press CTRL+Z to exit"

class Target:

  def __init__(self):
    self.capture = cv.CaptureFromCAM(0)
    #cv.NamedWindow("Target", 1)

  def run(self):
    # Capture first frame to get size
    frame = cv.QueryFrame(self.capture)
    frame_size = cv.GetSize(frame)
    color_image = cv.CreateImage(cv.GetSize(frame), 8, 3)
    grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
    moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
    tracking = False

    first = True

    while True:
      closest_to_left = cv.GetSize(frame)[0]
      closest_to_right = cv.GetSize(frame)[1]

      color_image = cv.QueryFrame(self.capture)

      # Smooth to get rid of false positives
      cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)

      if first:
        difference = cv.CloneImage(color_image)
        temp = cv.CloneImage(color_image)
        cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
        first = False
      else:
        cv.RunningAvg(color_image, moving_average, 0.020, None)

      # Convert the scale of the moving average.
      cv.ConvertScale(moving_average, temp, 1.0, 0.0)

      # Minus the current frame from the moving average.
      cv.AbsDiff(color_image, temp, difference)

      # Convert the image to grayscale.
      cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)

      # Convert the image to black and white.
      cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

      # Dilate and erode to get people blobs
      cv.Dilate(grey_image, grey_image, None, 18)
      cv.Erode(grey_image, grey_image, None, 10)

      storage = cv.CreateMemStorage(0)
      contour = cv.FindContours(grey_image, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
      points = []

      while contour:
        bound_rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()

        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
        points.append(pt1)
        points.append(pt2)
        #cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)

      if len(points):
        tracking = True
        center_point = reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
        #cv.Circle(color_image, center_point, 40, cv.CV_RGB(255, 255, 255), 1)
        #cv.Circle(color_image, center_point, 30, cv.CV_RGB(255, 100, 0), 1)
        #cv.Circle(color_image, center_point, 20, cv.CV_RGB(255, 255, 255), 1)
        #cv.Circle(color_image, center_point, 10, cv.CV_RGB(255, 100, 0), 1)
                
        if (center_point[0] < 50):
          #plotDif(lookRight0,lookLeft1)
          plotRaw(lookRight0bL,lookRight1bR)
        elif (center_point[0] >= 30) and (center_point[0] < 101):
          #plotDif(lookRight0,lookLeft0)
          plotRaw(lookRight0bL,lookRight0bR)
        elif (center_point[0] >= 215) and (center_point[0] < 285):
          #plotDif(lookLeft0,lookRight0)
          plotRaw(lookLeft0bL,lookLeft0bR)
        elif (center_point[0] >= 285):
          #plotDif(lookLeft1,lookRight0)
          plotRaw(lookLeft1bL,lookLeft0bR)
        else:
          #plot(gaze)
          plotRaw(gazebL,gazebR)
      else:
          if tracking:
            tracking = False
            #blink()
            blinkb()
          #plot(gaze)
          plotRaw(gazebL,gazebR)
      #cv.ShowImage("Target", color_image)
      # Listen for ESC key
      c = cv.WaitKey(7) % 0x100
      if c == 27:
        break



#Animation Frames
r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 1,1,1,1,0,0,0,0
r3 = 0,1,1,1,0,1,1,0
r4 = 0,0,1,1,0,1,1,1
r5 = 0,0,0,1,1,1,1,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
gaze = r0,r1,r2,r3,r4,r5,r6,r7

r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 1,1,1,1,0,0,0,0
r3 = 0,1,1,0,1,1,1,0
r4 = 0,0,1,0,1,1,1,1
r5 = 0,0,0,0,1,1,1,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
lookLeft0 = r0,r1,r2,r3,r4,r5,r6,r7


r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 1,1,0,1,0,0,0,0
r3 = 0,1,0,1,1,1,1,0
r4 = 0,0,0,1,1,1,1,1
r5 = 0,0,0,1,1,1,1,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
lookLeft1 = r0,r1,r2,r3,r4,r5,r6,r7

r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 1,1,1,1,0,0,0,0
r3 = 0,1,1,1,1,1,0,0
r4 = 0,0,1,1,1,1,0,1
r5 = 0,0,0,1,1,1,0,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
lookRight0 = r0,r1,r2,r3,r4,r5,r6,r7

r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 1,1,1,1,0,0,0,0
r3 = 0,1,1,1,1,1,0,0
r4 = 0,0,1,1,1,1,0,0
r5 = 0,0,0,1,1,1,1,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
lookRight1 = r0,r1,r2,r3,r4,r5,r6,r7

r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 0,0,0,0,0,0,0,0
r3 = 0,0,0,0,0,0,0,0
r4 = 0,0,1,1,0,1,1,1
r5 = 0,0,0,1,1,1,1,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
sleepy = r0,r1,r2,r3,r4,r5,r6,r7

r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 0,0,0,0,0,0,0,0
r3 = 0,1,1,1,0,0,0,0
r4 = 0,0,1,1,0,1,1,1
r5 = 0,0,0,1,1,1,1,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
blink0 = r0,r1,r2,r3,r4,r5,r6,r7

r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 0,0,0,0,0,0,0,0
r3 = 0,0,0,0,0,0,0,0
r4 = 0,0,1,1,0,1,1,1
r5 = 0,0,0,0,0,0,0,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
blink1 = r0,r1,r2,r3,r4,r5,r6,r7

r0 = 0,0,1,1,1,1,1,0
r1 = 0,1,1,1,1,1,1,1
r2 = 1,1,1,1,0,1,1,1
r3 = 0,1,1,1,0,1,1,1
r4 = 0,0,1,1,0,1,1,1
r5 = 0,0,0,1,1,1,1,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
surprised = r0,r1,r2,r3,r4,r5,r6,r7

r0 = 0,0,0,0,0,0,0,0
r1 = 0,0,0,0,0,0,0,0
r2 = 0,0,0,0,0,0,0,0
r3 = 0,0,0,0,0,0,0,0
r4 = 0,0,0,0,0,0,0,0
r5 = 0,0,0,0,0,0,0,0
r6 = 0,0,0,0,0,0,0,0
r7 = 0,0,0,0,0,0,0,0
empty = r0,r1,r2,r3,r4,r5,r6,r7

#---bitmaps----

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b01111000
r4 = 0b00110111
r3 = 0b10010111
r2 = 0b00000111
r1 = 0b00000000
r0 = 0b00000000
lookLeft0bL = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b10000111
r4 = 0b00111011
r3 = 0b01111010
r2 = 0b00111000
r1 = 0b00000000
r0 = 0b00000000
lookRight0bR = r0,r1,r2,r3,r4,r5,r6,r7


r7 = 0b00000000
r6 = 0b00000000
r5 = 0b01101000
r4 = 0b00101111
r3 = 0b10001111
r2 = 0b00001111
r1 = 0b00000000
r0 = 0b00000000
lookLeft1bL = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b10000101
r4 = 0b00111101
r3 = 0b01111100
r2 = 0b00111100
r1 = 0b00000000
r0 = 0b00000000
lookRight1bR = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b01111000
r4 = 0b00111110
r3 = 0b10011110
r2 = 0b00001110
r1 = 0b00000000
r0 = 0b00000000
lookRight0bL = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b10000111
r4 = 0b00011111
r3 = 0b01011110
r2 = 0b00011100
r1 = 0b00000000
r0 = 0b00000000
lookLeft0bR = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b00000000
r4 = 0b00111000
r3 = 0b10011011
r2 = 0b00001111
r1 = 0b00000000
r0 = 0b00000000
blink0bL = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b00000000
r4 = 0b00110111
r3 = 0b01110110
r2 = 0b00111100
r1 = 0b00000000
r0 = 0b00000000
blink0bR = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b00000000
r4 = 0b00000000
r3 = 0b10011011
r2 = 0b00000000
r1 = 0b00000000
r0 = 0b00000000
blink1bL = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b00000000
r4 = 0b00000000
r3 = 0b01110110
r2 = 0b00000000
r1 = 0b00000000
r0 = 0b00000000
blink1bR = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b01111000
r4 = 0b00111011
r3 = 0b10011011
r2 = 0b00001111
r1 = 0b00000000
r0 = 0b00000000
gazebL = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b10000111
r4 = 0b00110111
r3 = 0b01110110
r2 = 0b00111100
r1 = 0b00000000
r0 = 0b00000000
gazebR = r0,r1,r2,r3,r4,r5,r6,r7

r7 = 0b00000000
r6 = 0b00000000
r5 = 0b00000000
r4 = 0b00000000
r3 = 0b00000000
r2 = 0b00000000
r1 = 0b00000000
r0 = 0b00000000
emptyb = r0,r1,r2,r3,r4,r5,r6,r7


def flip(v):
  return 7-v

def plot(state):
  #leftEye.clear()
  for x in range(6, 1,-1):
    for y in range(7, -1,-1):
      if state[x][y] == 1:
        rightEye.setPixel(y,flip(x))
        leftEye.setPixel(flip(y), flip(x))
      else:
        rightEye.clearPixel(y,flip(x))
        leftEye.clearPixel(flip(y), flip(x))
        
def plotWhole(state):
  for x in range(7, -1, -1):
    for y in range(7, -1, -1):
      if state[x][y] == 1:
        rightEye.setPixel(y,flip(x))
        leftEye.setPixel(flip(y), flip(x))
      else:
        rightEye.clearPixel(y,flip(x))
        leftEye.clearPixel(flip(y), flip(x))
        
def plotDif(leftState,rightState):
  for x in range(6, 1, -1):
    for y in range(7, -1, -1):
      if leftState[x][y] == 1:
        leftEye.setPixel(flip(y), flip(x))
      else:
        leftEye.clearPixel(flip(y), flip(x))
      if rightState[x][y] == 1:
        rightEye.setPixel(y,flip(x))
      else:
        rightEye.clearPixel(y, flip(x))
        
def plotRaw(rawsLeft,rawsRight):
  for i in range(0, 8, 1):
    leftEye.writeRowRaw(i,rawsLeft[i])
    rightEye.writeRowRaw(i,rawsRight[i])

def clearLookPupil():
  clearPixels = [[3,3],[3,4],[3,5],[2,2],[2,3],[2,4],[6,3],[6,4],[6,5]]
  for i in range(0,8):
    rightEye.setPixel(clearPixels[i][1],flip(clearPixels[i][0]))
    leftEye.setPixel(flip(clearPixels[i][1]), flip(clearPixels[i][0]))

  

rate = .000001  

def blink():
  leftEye.disp.setBrightness(3)
  rightEye.disp.setBrightness(3)
  plot(blink0)
  leftEye.disp.setBrightness(1)
  rightEye.disp.setBrightness(1)
  plot(blink1)
  leftEye.disp.setBrightness(0)
  rightEye.disp.setBrightness(0)
  plot(empty)
  plot(blink1)
  leftEye.disp.setBrightness(1)
  rightEye.disp.setBrightness(1)
  leftEye.disp.setBrightness(3)
  rightEye.disp.setBrightness(3)
  plot(blink0)
  plot(gaze)
  leftEye.disp.setBrightness(defaultBright)
  rightEye.disp.setBrightness(defaultBright)
  
def blinkb():
  leftEye.disp.setBrightness(3)
  rightEye.disp.setBrightness(3)
  plotRaw(blink0bL,blink0bR)
  leftEye.disp.setBrightness(1)
  rightEye.disp.setBrightness(1)
  plotRaw(blink1bL,blink1bR)
  leftEye.disp.setBrightness(0)
  rightEye.disp.setBrightness(0)
  plotRaw(blink1bL,blink1bR)
  leftEye.disp.setBrightness(1)
  rightEye.disp.setBrightness(1)
  plotRaw(blink0bL,blink0bR)
  leftEye.disp.setBrightness(3)
  rightEye.disp.setBrightness(3)
  plotRaw(blink0bL,blink0bR)
  plotRaw(gazebL,gazebR)
  leftEye.disp.setBrightness(defaultBright)
  rightEye.disp.setBrightness(defaultBright)
  
def openEyes():
  plot(empty)
  plot(blink1)
  plot(blink0)
  plot(gaze)
  
def lookLeft():
  plotDif(lookLeft0,lookRight0)
  plotDif(lookLeft1,lookRight0)
  time.sleep(1)
  plotDif(lookLeft0,lookRight0)

def lookRight():
  plotDif(lookRight0,lookLeft0)
  plotDif(lookRight0,lookLeft1)
  time.sleep(1)
  plotDif(lookRight0,lookLeft0)
  
def surprise(length):
  plotWhole(surprised)
  time.sleep(length)
  plotWhole(gaze)

def peek(t):
  plot(blink1)
  plot(sleepy)
  time.sleep(t)
  plot(blink1)
  plot(empty)


def awaken():
  plot(empty)
  time.sleep(3)
  peek(3)
  time.sleep(3)
  peek(2)

  time.sleep(2)
  openEyes()

leftEye.disp.setBrightness(defaultBright)
rightEye.disp.setBrightness(defaultBright)
plotRaw(gazebL,gazebR)
if __name__=="__main__":
    t = Target()
    t.run()



