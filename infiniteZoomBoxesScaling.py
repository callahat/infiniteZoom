from gimpfu import *

# This method is for planning.
# finalXOrg and finalYOrg are the coordinates for the top left rectangle that will be the smallest
#     rectangle
# scale will be how how small to reduce the original image by (ie, smallest would be 1/<scale>, 
#     and be at (finalXOrg, finalYOrg)
# steps - the number of times the original image will be scaled down incrementally to reach the smallest size
# Your image will have a new layer with these rectangles drawn onto one layer
def infiniteZoomBoxesScaling(img, referenceLayer, finalXOrg, finalYOrg, scale, steps=-1) :
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
    
    scaledBoxesRef = referenceLayer.copy()
    scaledBoxesRef.name = 'scaleboxesRef'
    
    print("Adding " + scaledBoxesRef.name + " to img")
    img.add_layer(scaledBoxesRef, 0)
    
    scaledBoxes = referenceLayer.copy()
    scaledBoxes.name = 'scaleboxes'
    
    print("Adding " + scaledBoxes.name + " to img")
    img.add_layer(scaledBoxes, 0)
    
    # Top left is 0,0
    
    xLeftRange = finalXOrg
    xRightRange = finalXOrg + scaledWidth
    yTopRange = finalYOrg
    yDownRange = finalYOrg + scaledHeight
    
    pdb.gimp_pencil(scaledBoxes, 4, [0,0,                xLeftRange,yTopRange])
    pdb.gimp_pencil(scaledBoxes, 4, [0,oldHeight,        xLeftRange,yDownRange])
    pdb.gimp_pencil(scaledBoxes, 4, [oldWidth,0,         xRightRange,yTopRange])
    pdb.gimp_pencil(scaledBoxes, 4, [oldWidth,oldHeight, xRightRange,yDownRange])
    
    pdb.gimp_pencil(scaledBoxes, 10, [xLeftRange,yTopRange,
        xRightRange,yTopRange,
        xRightRange,yDownRange,
        xLeftRange,yDownRange,
        xLeftRange,yTopRange])
    
    for step in range(0, steps - 2):
        #currLayer = referenceLayer.copy()
        #currLayer.name = 'scaleboxes'
        
        #print("Adding " + currLayer.name + " to img")
        #img.add_layer(currLayer, 0)
        
        xLeftRangeD = xLeftRange - xLeftRange * step / steps
        xRightRangeD = xRightRange + (oldWidth - xRightRange) * step / steps
        yTopRangeD = yTopRange - yTopRange * step / steps
        yDownRangeD = yDownRange + (oldHeight - yDownRange) * step / steps
        
        print("**********" + str((step)))
        print("Selecting " + str((xLeftRangeD," x ",yTopRangeD)))
        print("Dim       " + str((xRightRangeD-xLeftRangeD," x ",yDownRangeD-yTopRangeD)))
        
        
        pdb.gimp_rect_select(img, xLeftRangeD, yTopRangeD, xRightRangeD-xLeftRangeD, yDownRangeD-yTopRangeD, 2, 0, 0)
        non_empty = pdb.gimp_edit_copy(scaledBoxes)
        floating_sel = pdb.gimp_edit_paste(scaledBoxes, 0)
        xOff,yOff = floating_sel.offsets
        
        print("Offsets:    " + str((xOff," x ",yOff)))
        floating_sel.translate(-xOff,-yOff)
        print("Scaling to: " + str((oldWidth," x ",oldHeight)))
        floating_sel.scale(oldWidth,oldHeight,0)
        pdb.gimp_floating_sel_to_layer(floating_sel)
        
        pdb.gimp_pencil(scaledBoxesRef, 10, [xLeftRangeD,yTopRangeD,
        xRightRangeD,yTopRangeD,
        xRightRangeD,yDownRangeD,
        xLeftRangeD,yDownRangeD,
        xLeftRangeD,yTopRangeD])
        
    pdb.gimp_context_set_brush( old_brush )

infiniteZoomBoxesScaling(img, layer, 1118, 760, 172, 5)
