scaling_types = [squareCoef]

def generateWithAllTypes(image, scalingTypes, frames=30 ) :
    for scaling_type in scalingTypes :
        print('++++++++++++++++++++++++++++++++++++++++')
        print('Scaling using ' + scaling_type.__name__)
        new_image = pdb.gimp_image_duplicate(image)
        refLayer = new_image.layers[0]
        
        infiniteZoom(new_image, refLayer, 1118, 760, 172, scaling_type, frames)
        pdb.gimp_image_set_filename(new_image, scaling_type.__name__ + '.jpg')
        display = pdb.gimp_display_new(new_image)
