import unittest
import numpy

import math

def generateRectangleCoordinates(width, height, targetWidth, targetHeight, targetX, targetY, how, steps=1) :
    xLeft = targetX
    xRight = targetX + targetWidth
    yTop = targetY
    yDown = targetY + targetHeight
    
    xCenter = (xLeft + xRight) / 2.0
    yCenter = (yTop + yDown) / 2.0
    
    coords =       []
    selectCoords = []
    
    for step in range(0, steps):
        xResizedLeft = xLeft - xLeft * how(step, steps)
        xResizedRight = xRight + (width - xRight) * how(step, steps)
        yResizedTop = yTop - yTop * how(step, steps)
        yResizedDown = yDown + (height - yDown) * how(step, steps)
        
        xSelectLeft = xCenter - xCenter / ( (xCenter-xResizedLeft) / float(xCenter-xLeft) )
        xSelectRight = xCenter + (width - xCenter) / ( (xResizedRight-xCenter) / float(xRight-xCenter) )
        ySelectTop = yCenter - yCenter / ( (yCenter-yResizedTop) / float(yCenter-yTop))
        ySelectDown = yCenter + (height - yCenter) / ((yResizedDown-yCenter) / float(yDown-yCenter))
        
        coords.append( [xResizedLeft, xResizedRight, yResizedTop, yResizedDown] )
        selectCoords.append( [xSelectLeft, xSelectRight, ySelectTop, ySelectDown] )
    return [coords, selectCoords]

def linearCoef(step, steps) :
    return step / float(steps)

def inverseLogCoef(step, steps) :
    return (1 - math.log(step+1) / (math.log(steps+1) + 0.00001) )

def inverseRoot(step, steps) :
    return (1-math.sqrt(steps-step) / max(1.0,math.sqrt(steps)))

def inverseRoot2(step, steps) :
    return (1-math.pow(step-steps,2) / max(1.0,math.pow(steps,2)))

def squareCoef(step, steps) :
     return math.pow(step,2) / max(1.0,math.pow(steps,2))


rectCoords, selCoords = generateRectangleCoordinates(2592,1944,15,11,1100,760,linearCoef,5)

def rountArrayOf4Floats( arrayOfFloats ):
    return map( (lambda x: int(round(x))),arrayOfFloats )

def rountArrayOfArrayOf4Floats( arrayOf4Floats ):
    return map( (lambda x: rountArrayOf4Floats(x)),arrayOf4Floats )

expectedCoords =    [[1100, 1115, 760,  771], [ 880, 1410, 608, 1006], [ 660, 1706, 456, 1240], [ 440, 2001, 304, 1475], [ 220, 2297, 152, 1709]]
expectedSelCoords = [[   0, 2592,   0, 1944], [1071, 1144, 739,  792], [1089, 1126, 752,  779], [1095, 1120, 756,  775], [1098, 1117, 759,  772]]

appxRectCoords = rountArrayOfArrayOf4Floats(rectCoords)
appxSelCoords =  rountArrayOfArrayOf4Floats(selCoords)

class HelperTests(unittest.TestCase):
    def testCoords(self):
        numpy.testing.assert_array_equal(appxRectCoords, expectedCoords)
    
    def testSelCoords(self):
        numpy.testing.assert_array_equal(appxSelCoords, expectedSelCoords)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
