def test_geometry1d():
    import geotechnics as gt
    slib = gt.SoilLib()
    slib.add_soiltype(name="klei_14", ydry=14., ysat=14.)
    slib.add_soiltype(name="veen_10", ydry=10., ysat=10.)
    slib.add_soiltype(name="zand_17", ydry=17., ysat=19.)

    #start a geometry
    g = gt.Geometry1D(soillib=slib)
    print "Adding 3 layers"
    g.add_layer(gt.Layer1D(top=0., bottom=-2., soilname="klei_14"))
    g.add_layer(gt.Layer1D(bottom=-4., soilname="veen_10"))
    g.add_layer(gt.Layer1D(bottom=-7., soilname="zand_17"))
    print("Checking if we have added 3 layers")
    g.print_layers()
    assert g.num_layers()==3
    print("----------------------------------------------------------------------")

    #add an invalid soilname
    print("Checking if it is not possible to add an invalid soilname zand_171")
    g.add_layer(gt.Layer1D(bottom=-7., soilname="zand_171"))
    assert g.num_layers()==3
    print("----------------------------------------------------------------------")

    #add an invalid layer
    print("Checking if it is not possible to add a layer higher than the lowest one (bottom=-6, soilname=zand_17)")
    g.add_layer(gt.Layer1D(bottom=-6., soilname="zand_17"))
    assert g.num_layers()==3
    print("----------------------------------------------------------------------")

    #insert a layer within one big layer (valid)
    print("Check if we can insert a new layer -2 to -6.7 zand_17")
    print("Note that this will merge the last two sandlayers to -7")
    g.insert_layer(gt.Layer1D(top=-2.0, bottom=-6.7, soilname="zand_17"))
    g.print_layers()
    assert g.num_layers()==2
    print("----------------------------------------------------------------------")

    #insert a layer within
    print("Check if we can insert a new layer -1.5 to -3 veen_10")
    g.insert_layer(gt.Layer1D(top=-1.5, bottom=-3.0, soilname="veen_10"))
    g.print_layers()
    assert g.num_layers()==3
    print("----------------------------------------------------------------------")
