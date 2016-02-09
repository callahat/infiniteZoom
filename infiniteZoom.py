from gimpfu import *

def infiniteZoom(img, referenceLayer, finalXOrg, finalYOrg, scale) :
    old_brush = pdb.gimp_context_get_brush()
    pdb.gimp_context_set_brush('Circle (01)')

    print("Starting infiniZoom")

    SCALINGS = 6

    oldWidth = layer.width
    oldHeight = layer.height

    scaledWidth = layer.width / scale
    scaledHeight = layer.height / scale

    print("Full image is " + str((oldWidth," x ",oldHeight)))
    print("Image will be scaled to " + str((scaledWidth, " x ", scaledHeight)))

    currLayer = layer.copy()
    currLayer.name = 'scaleboxes'

    pdb.gimp_pencil(currLayer, 10, [1118,760,1118+15,760,1118+15,760+11,1118,760+11,1118,760])

    print("Adding " + currLayer.name + " to img")
    img.add_layer(currLayer, 0)

    for layerCnt in range(0, totalFrames+1):
        xLeft = 0
        xRight = 0
        yUp = 0
        yDown = 0


        pdb.gimp_pencil(currLayer, 10, [1118,760,1118+15,760,1118+15,760+11,1118,760+11,1118,760])

    pdb.gimp_context_set_brush( old_brush )
