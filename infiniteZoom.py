from gimpfu import *

import math

def generateRectangleCoordinates(width, height, targetWidth, targetHeight, targetX, targetY, steps=1) :
    coords = []
    
    xLeftRange = targetX
    xRightRange = targetX + targetWidth
    yTopRange = targetY
    yDownRange = targetY + targetHeight
    
    for step in range(0, steps):
        xLeftRangeD = xLeftRange - xLeftRange * step / steps
        xRightRangeD = xRightRange + (width - xRightRange) * step / steps
        yTopRangeD = yTopRange - yTopRange * step / steps
        yDownRangeD = yDownRange + (height - yDownRange) * step / steps
        
        coords.append( [xLeftRangeD, xRightRangeD, yTopRangeD, yDownRangeD] )
    return coords

# assumes the first set of rectangle coordinates is 
def generateSelectBoxesFromCoordinates(width, height, rectangleCoordinates) :
    xInitLeft, xInitRight, yInitTop, yInitDown = rectangleCoordinates[0]
    xCenter = (xInitLeft + xInitRight) / 2.0
    yCenter = (yInitTop + yInitDown) / 2.0
    
    print("Center:" + str((xCenter,yCenter)))
    
    print('here')
    print(xInitLeft)
    print(xInitRight)
    print(yInitTop)
    print(yInitDown)
    
    selectCoords = [ [xInitLeft, xInitRight, yInitTop, yInitDown] ]
    
    for coords in rectangleCoordinates[1:] :
        print(coords)
        xResizedLeft, xResizedRight, yResizedTop, yResizedDown = coords
        
        xSelectLeft = xCenter - xCenter / ( (xCenter-xResizedLeft) / float(xCenter-xInitLeft) )
        xSelectRight = xCenter + (width - xCenter) / ( (xResizedRight-xCenter) / float(xInitRight-xCenter) )
        
        ySelectTop = yCenter - yCenter / ( (yCenter-yResizedTop) / float(yCenter-yInitTop))
        ySelectDown = yCenter + (height - yCenter) / ((yResizedDown-yCenter) / float(yInitDown-yCenter))
        
        
        print('select coord')
        print(xSelectLeft)
        print(xSelectRight)
        print(ySelectTop)
        print(ySelectDown)
        
        selectCoords.append( [xSelectLeft, xSelectRight, ySelectTop, ySelectDown] )
    return selectCoords

# reference Layer will be the image that will be scaled (such as background)
# finalXOrg and finalYOrg are the coordinates for the top left rectangle that will be the smallest
#     rectangle
# scale will be how how small to reduce the original image by (ie, smallest would be 1/<scale>, 
#     and be at (finalXOrg, finalYOrg)
# steps - the number of times the original image will be scaled down incrementally to reach the smallest size
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

def infiniteZoom(img, referenceLayer, finalXOrg, finalYOrg, scale, how, steps=15) :
    
    old_brush = pdb.gimp_context_get_brush()
    pdb.gimp_context_set_brush('Circle (01)')
    
    print("Starting infiniZoom")
    
    oldWidth = referenceLayer.width
    oldHeight = referenceLayer.height
    
    scaledWidth = referenceLayer.width / float(scale)
    scaledHeight = referenceLayer.height / float(scale)
    
    if steps == -1 :
        print("Number of steps not passed in, using based on size of the smallest rectangle. This may take a while")
        steps = oldWidth / scaledWidth
    
    print("Number of steps: " + str((steps)))
    
    print("Full image is " + str((oldWidth," x ",oldHeight)))
    print("Image will be scaled to " + str((scaledWidth, " x ", scaledHeight)))
    
    xLeftRange = finalXOrg
    xRightRange = finalXOrg + scaledWidth
    yTopRange = finalYOrg
    yDownRange = finalYOrg + scaledHeight
    
    for step in range(0, steps ):
        print("Step " + str(step))
        xLeftSelect = xLeftRange - xLeftRange * how(step, steps)
        xRightSelect = xRightRange + (oldWidth - xRightRange) * how(step, steps)
        yTopSelect = yTopRange - yTopRange * how(step, steps)
        yDownSelect = yDownRange + (oldHeight - yDownRange) * how(step, steps)
        
        print("**********" + str((step)))
        print("Selecting " + str((xLeftSelect," x ",yTopSelect)))
        print("Dim       " + str((xRightSelect-xLeftSelect," x ",yDownSelect-yTopSelect)))
        
        pdb.gimp_rect_select(img, xLeftSelect, yTopSelect, xRightSelect-xLeftSelect, yDownSelect-yTopSelect, 2, 0, 0)
        non_empty = pdb.gimp_edit_copy(referenceLayer)
        floating_sel = pdb.gimp_edit_paste(referenceLayer, 0)
        xOff,yOff = floating_sel.offsets
        
        print("Offsets:    " + str((xOff," x ",yOff)))
        floating_sel.translate(-xOff,-yOff)
        print("Scaling to: " + str((oldWidth," x ",oldHeight)))
        floating_sel.scale(oldWidth,oldHeight,0)
        pdb.gimp_floating_sel_to_layer(floating_sel)
        floating_sel.name = "Step " + str(step)
        
        selectWidth = xRightSelect-xLeftSelect
        selectHeight = yDownSelect-yTopSelect
        
        scalarX = oldWidth  / selectWidth
        scalarY = oldHeight / selectHeight
        
        smallerNewX = scalarX * (finalXOrg - xLeftSelect)
        smallerNewY = scalarY * (finalYOrg - yTopSelect)
        
        print("Scalar: " + str((scalarX," x ",scalarY)))
        
        smallerImage = referenceLayer.copy()
        img.add_layer(smallerImage, 0)
        smallerImage.scale(scalarX * scaledWidth,scalarY * scaledHeight,0)
        smallerImage.translate(smallerNewX, smallerNewY)
        pdb.gimp_image_merge_down(img, smallerImage, 0)
        
    pdb.gimp_context_set_brush( old_brush )
