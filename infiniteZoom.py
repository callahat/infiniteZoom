from gimpfu import *

import math

def drawBox(layer, xLeftRangeD, xRightRangeD, yTopRangeD, yDownRangeD) :
    pdb.gimp_pencil(layer, 10, [xLeftRangeD,yTopRangeD,
        xRightRangeD,yTopRangeD,
        xRightRangeD,yDownRangeD,
        xLeftRangeD,yDownRangeD,
        xLeftRangeD,yTopRangeD])

def drawBoxRed(layer, xLeftRangeD, xRightRangeD, yTopRangeD, yDownRangeD) :
    old_foreground = pdb.gimp_context_get_foreground()
    pdb.gimp_context_set_foreground((255,0,0))
    drawBox(layer, xLeftRangeD, xRightRangeD, yTopRangeD, yDownRangeD)
    pdb.gimp_context_set_foreground(old_foreground)

def drawBoxWhite(layer, xLeftRangeD, xRightRangeD, yTopRangeD, yDownRangeD) :
    old_foreground = pdb.gimp_context_get_foreground()
    pdb.gimp_context_set_foreground((255,255,255))
    drawBox(layer, xLeftRangeD, xRightRangeD, yTopRangeD, yDownRangeD)
    pdb.gimp_context_set_foreground(old_foreground)

def generateRectangleCoordinates(width, height, targetWidth, targetHeight, targetX, targetY, how, steps=1) :
    xLeft = targetX
    xRight = targetX + targetWidth
    yTop = targetY
    yDown = targetY + targetHeight
    
    xCenter = (xLeft + xRight) / 2.0
    yCenter = (yTop + yDown) / 2.0
    
    coords = []
    
    for step in range(0, steps+1):
        xResizedLeft = xLeft - xLeft * how(step, steps)
        xResizedRight = xRight + (width - xRight) * how(step, steps)
        yResizedTop = yTop - yTop * how(step, steps)
        yResizedDown = yDown + (height - yDown) * how(step, steps)
        
        coords.append( [xResizedLeft, xResizedRight, yResizedTop, yResizedDown] )
    
    return coords

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
    
    resizeCoords = generateRectangleCoordinates(oldWidth,oldHeight,scaledWidth,scaledHeight,finalXOrg,finalYOrg,how,steps)
    
    drawBoxWhite(referenceLayer, finalXOrg,finalXOrg+scaledWidth,finalYOrg,finalYOrg+scaledHeight)
    
    selCords = list(resizeCoords)
    selCords.reverse()
    
    print("resize - Number of coords for " + str((steps)) + " steps:" + str((len(resizeCoords))))
    print("select - Number of coords for " + str((steps)) + " steps:" + str((len(selCords))))
    
    #for i in range(0, len(resizeCoords)):
    #    xLeftSelect,xRightSelect,yTopSelect,yDownSelect = selCords[i]
    #    xLeftResize,xRightResize,yTopResize,yDownResize = resizeCoords[i]
    #    
    #    smallerImage = referenceLayer.copy()
    #    img.add_layer(smallerImage, 0)
    #    
    #    drawBox(smallerImage, xLeftSelect,xRightSelect,yTopSelect,yDownSelect)
    #    drawBoxRed(smallerImage, xLeftResize,xRightResize,yTopResize,yDownResize)
    
    for i in range(0, len(resizeCoords)):
        xLeftSelect,xRightSelect,yTopSelect,yDownSelect = selCords[i]
    
        print("Step " + str(i))
        
        print("**********" + str((i)))
        print("Selecting " + str((xLeftSelect," x ",yTopSelect)))
        print("Dim       " + str((xRightSelect-xLeftSelect," x ",yDownSelect-yTopSelect)))
        
        pdb.gimp_rect_select(img, xLeftSelect, yTopSelect, xRightSelect-xLeftSelect, yDownSelect-yTopSelect, 2, 0, 0)
        print("where that error coming from")
        non_empty = pdb.gimp_edit_copy(referenceLayer)
        floating_sel = pdb.gimp_edit_paste(referenceLayer, 0)
        xOff,yOff = floating_sel.offsets
        
        print("Offsets:    " + str((xOff," x ",yOff)))
        floating_sel.translate(-xOff,-yOff)
        print("Scaling to: " + str((oldWidth," x ",oldHeight)))
        floating_sel.scale(oldWidth,oldHeight,0)
        print("here 1")
        pdb.gimp_floating_sel_to_layer(floating_sel)
        print("here 2")
        floating_sel.name = "Step " + str((i))
        
        xLeftResize,xRightResize,yTopResize,yDownResize = resizeCoords[i]
        
        selectWidth = xRightResize-xLeftResize
        selectHeight = yDownResize-yTopResize
        
        print("Scaling down to:" + str((selectWidth," x ", selectHeight)))
        
        smallerImage = referenceLayer.copy()
        img.add_layer(smallerImage, 0)
        print("here 2.5 ")
        smallerImage.scale(selectWidth,selectHeight,0)
        print("here 3")
        smallerImage.translate(xLeftResize, yTopResize)
        print("here 4")
        pdb.gimp_image_merge_down(img, smallerImage, 0)
        print("here 5")
        
    pdb.gimp_context_set_brush( old_brush )

infiniteZoom(img, layer, 1118, 760, 172, linearCoef, 5)
