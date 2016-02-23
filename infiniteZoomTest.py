import unittest

import math

def generateRectangleCoordinates(width, height, targetWidth, targetHeight, targetX, targetY, steps=1) :
    xLeft = targetX
    xRight = targetX + targetWidth
    yTop = targetY
    yDown = targetY + targetHeight
    
    xCenter = (xLeft + xRight) / 2.0
    yCenter = (yTop + yDown) / 2.0
    
    coords =       [ [xLeft, xRight, yTop, yDown] ]
    selectCoords = [ [xLeft, xRight, yTop, yDown] ]
    
    for step in range(1, steps):
        xResizedLeft = xLeft - xLeft * step / steps
        xResizedRight = xRight + (width - xRight) * step / steps
        yResizedTop = yTop - yTop * step / steps
        yResizedDown = yDown + (height - yDown) * step / steps
        
        xSelectLeft = xCenter - xCenter / ( (xCenter-xResizedLeft) / float(xCenter-xLeft) )
        xSelectRight = xCenter + (width - xCenter) / ( (xResizedRight-xCenter) / float(xRight-xCenter) )
        ySelectTop = yCenter - yCenter / ( (yCenter-yResizedTop) / float(yCenter-yTop))
        ySelectDown = yCenter + (height - yCenter) / ((yResizedDown-yCenter) / float(yDown-yCenter))
        
        coords.append( [xResizedLeft, xResizedRight, yResizedTop, yResizedDown] )
        selectCoords.append( [xSelectLeft, xSelectRight, ySelectTop, ySelectDown] )
    return [coords, selectCoords]

rectCoords, selCoords = generateRectangleCoordinates(2592,1944,15,11,1100,760,5)

expectedCoords = [[1100, 1115, 760, 771], [1100, 1115, 760, 771], [880, 1410, 608, 1005], [660, 1705, 456, 1240], [440, 2001, 304, 1474], [220, 2296, 152, 1709]]
expectedSelCoords = [[1100, 1115, 760, 771], [0.0, 2952.0, 0.0, 1944.0], [1070.9890109890109, 1153.2314049586778, 738.76825396825393, 792.56367432150319], [1088.9385474860335, 1130.6527196652719, 751.89660743134084, 779.16016859852482], [1095.056179775281, 1122.9826524902071, 756.37703141928489, 774.6485532815808], [1098.1408450704225, 1119.1396718552799, 758.63732681336592, 772.36989931107576]]

class HelperTests(unittest.TestCase):
    def testCoords(self):
        self.failIf(rectCoords == expectedCoords)
    
    def testSelCoords(self):
        self.failIf(selCoords == expectedSelCoords)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
