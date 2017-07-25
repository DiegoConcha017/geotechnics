def test_geometry1d():
    import geotechnics as gt
    slib = gt.SoilLib()
    slib.add_soiltype(name="klei_14", ydry=14., ysat=14.)
    slib.add_soiltype(name="veen_10", ydry=10., ysat=10.)
    slib.add_soiltype(name="zand_17", ydry=17., ysat=19.)

    #start a geometry
    g = gt.geometry.Geometry1D(soillib=slib)
    print "Adding 3 layers"
    g.add_layer(gt.geometry.Layer1D(top=0., bottom=-2., soilname="klei_14"))
    g.add_layer(gt.geometry.Layer1D(bottom=-4., soilname="veen_10"))
    g.add_layer(gt.geometry.Layer1D(bottom=-7., soilname="zand_17"))
    print("Checking if we have added 3 layers")
    g.print_layers()
    assert g.num_layers()==3
    print("--------------------------------------------------------------------------------")

    #add an invalid soilname
    print("Checking if it is not possible to add an invalid soilname zand_171")
    g.add_layer(gt.geometry.Layer1D(bottom=-7., soilname="zand_171"))
    assert g.num_layers()==3
    print("--------------------------------------------------------------------------------")

    #add an invalid layer
    print("Checking if it is not possible to add a layer higher than the lowest one (bottom=-6, soilname=zand_17)")
    g.add_layer(gt.geometry.Layer1D(bottom=-6., soilname="zand_17"))
    assert g.num_layers()==3
    print("--------------------------------------------------------------------------------")

    #insert a layer within one big layer (valid)
    print("Check if we can insert a new layer -2 to -6.7 zand_17")
    print("Note that this will merge the last two sandlayers to -7")
    g.insert_layer(gt.geometry.Layer1D(top=-2.0, bottom=-6.7, soilname="zand_17"))
    g.print_layers()
    assert g.num_layers()==2
    assert g._layers[-1].bottom == -7.0
    print("--------------------------------------------------------------------------------")

    #insert a layer overlapping two layers
    print("Check if we can insert a new layer -1.5 to -3 veen_10")
    g.insert_layer(gt.geometry.Layer1D(top=-1.5, bottom=-3.0, soilname="veen_10"))
    g.print_layers()
    assert g.num_layers()==3
    assert g._layers[1].top == -1.5
    print("--------------------------------------------------------------------------------")

    #insert a layer within a layer
    print("Check if we can insert a new layer -4.5 to -6 klei_14")
    g.insert_layer(gt.geometry.Layer1D(top=-4.5, bottom=-6.0, soilname="klei_14"))
    g.print_layers()
    assert g.num_layers()==5
    assert g._layers[2].bottom == -4.5
    print("--------------------------------------------------------------------------------")

    #delete the 3rd layer from the top using topdown
    print("Check if we can delete the -3.0 to -4.5 zand_17 layer")
    print("We use the topdown method which should extend the layer on top to the bottom of the deleted layer")
    g.delete_layer(2, method='down')
    g.print_layers()
    assert g.num_layers()==4
    assert g._layers[1].bottom == -4.5
    print("--------------------------------------------------------------------------------")

    #delete the 3rd layer from the top using bottomup
    print("Check if we can delete the -4.5 to -6.0 klei_14 layer")
    print("We use the bottomup method which should extend the lower layer to the top of the deleted layer")
    g.delete_layer(2, method='up')
    g.print_layers()
    assert g.num_layers()==3
    assert g._layers[-1].top == -4.5
    print("--------------------------------------------------------------------------------")

    #deleting a non existing layer should not be possible
    print("Check if we can delete a non existing layer")
    g.delete_layer(10)
    assert g.num_layers()==3
    print("--------------------------------------------------------------------------------")

    #delete the 2nd layer from the top using mid
    print("Check if we can delete the -1.5 to -4.5 veen_10 layer")
    print("We use the mid method which should extend the lower and higher layer to the middle of the deleted layer")
    g.delete_layer(1, method='mid')
    g.print_layers()
    assert g.num_layers()==2
    assert g._layers[0].bottom == -3.0
    print("--------------------------------------------------------------------------------")

    #delete the top layer
    print("Check if we can delete the top layer which does not do anything with the method")
    g.delete_layer(0)
    g.print_layers()
    assert g.num_layers()==1
    assert g._layers[0].top == -3.
    print("--------------------------------------------------------------------------------")

    #try to delete the last layer
    print("Check if we can delete the last layer (should no be possible)")
    g.delete_layer(0)
    g.print_layers()
    assert g.num_layers()==1
    print("--------------------------------------------------------------------------------")
