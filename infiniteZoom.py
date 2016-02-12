from gimpfu import *

# reference Layer will be the image that will be scaled (such as background)
# finalXOrg and finalYOrg are the coordinates for the top left rectangle that will be the smallest
#     rectangle
# scale will be how how small to reduce the original image by (ie, smallest would be 1/<scale>, 
#     and be at (finalXOrg, finalYOrg)
# steps - the number of times the original image will be scaled down incrementally to reach the smallest size
def infiniteZoom(img, referenceLayer, finalXOrg, finalYOrg, scale, steps=15) :
    old_brush = pdb.gimp_context_get_brush()
    pdb.gimp_context_set_brush('Circle (01)')
    
    print("Starting infiniZoom")
    
    oldWidth = referenceLayer.width
    oldHeight = referenceLayer.height
    
    scaledWidth = referenceLayer.width / scale
    scaledHeight = referenceLayer.height / scale
    
    if steps == -1 :
        print("Number of steps not passed in, using based on size of the smallest rectangle. This may take a while")
        steps = oldWidth / scaledWidth
    
    print("Number of steps: " + str((steps)))
    
    print("Full image is " + str((oldWidth," x ",oldHeight)))
    print("Image will be scaled to " + str((scaledWidth, " x ", scaledHeight)))
    
    scaledBoxes = referenceLayer.copy()
    scaledBoxes.name = 'scaleboxes'
    
    print("Adding " + currLayer.name + " to img")
    img.add_layer(currLayer, 0)
    
    # Top left is 0,0
    
    xLeftRange = finalXOrg
    xRightRange = finalXOrg + scaledWidth
    yTopRange = finalYOrg
    yDownRange = finalYOrg + scaledHeight
    
    xLeftIncrement = xLeftRange * (steps - 1) / steps
    xRightIncrement = xRightRange * (steps - 1) / steps
    yTopIncrement = yTopRange * (steps - 1) / steps
    yDownIncrement = yDownRange * (steps - 1) / steps
    
    xCenter = xLeftRange + scaledWidth / 2.0
    yCenter = yTopRange + scaledHeight / 2.0
    
    print("Image will be centered at " + str((xCenter, " x ", yCenter)))
    
    pdb.gimp_pencil(scaledBoxes, 4, [0,0,                xLeftRange,yTopRange])
    pdb.gimp_pencil(scaledBoxes, 4, [0,oldHeight,        xLeftRange,yDownRange])
    pdb.gimp_pencil(scaledBoxes, 4, [oldWidth,0,         xRightRange,yTopRange])
    pdb.gimp_pencil(scaledBoxes, 4, [oldWidth,oldHeight, xRightRange,yDownRange])
    
    
    print("Adding " + scaledBoxes.name + " to img")
    img.add_layer(scaledBoxes, 0)
    
    pdb.gimp_pencil(scaledBoxes, 10, [xLeftRange,yTopRange,
        xRightRange,yTopRange,
        xRightRange,yDownRange,
        xLeftRange,yDownRange,
        xLeftRange,yTopRange])
    
    for step in range(0, steps):
        
        
        xLeftRangeD = xLeftRange - xLeftRange * step / steps
        xRightRangeD = xRightRange + (oldWidth - xRightRange) * step / steps
        yTopRangeD = yTopRange - yTopRange * step / steps
        yDownRangeD = yDownRange + (oldHeight - yDownRange) * step / steps
        
        xIncrease = xLeftRangeD + xRightRangeD
        yIncrease = yTopRangeD + yDownRangeD
        
        newWidth = oldWidth + xIncrease
        newHeight = oldHeight + yIncrease
        
        xCenterRatio = xCenter / oldWidth
        yCenterRatio = yCenter / oldHeight
        
        print("Scaled up to " + str((newWidth, " x ", newHeight)))
        print("New center is " + str((xCenterRatio*newWidth, " x ", yCenterRatio*newHeight)))
        print("New center is " + str((xCenter*newWidth/oldWidth, " x ", yCenter*newHeight/oldHeight)))
        
        currLayer.scale(newWidth,newHeight,0)
        currLayer.translate(xCenter-xCenter*newWidth/oldWidth,yCenter-yCenter*newHeight/oldHeight)
        img.crop(oldWidth, oldHeight)
        
        #Might be easier to select rectangle, copy image, paste to new layer and then scale the new layer
        
    
    pdb.gimp_context_set_brush( old_brush )

infiniteZoom(img, layer, 1118, 760, 172, 3)
