def test_geometry1d():
    import geotechnics as gt
    slib = gt.SoilLib()
    slib.add_soiltype(name="klei_14", ydry=14., ysat=14.)
    slib.add_soiltype(name="veen_10", ydry=10., ysat=10.)
    slib.add_soiltype(name="zand_17", ydry=17., ysat=19.)

    #start a geometry
    g = gt.Geometry1D(soillib=slib)
    g.init_layers(gt.Layer1D(top=0., bottom=-2., soilname="klei_14"))
    g.add_layer(gt.Layer1D(bottom=-4., soilname="veen_10"))
    g.add_layer(gt.Layer1D(bottom=-7., soilname="zand_17"))
    assert g.num_layers()==3

    #add an invalid soilname
    g.add_layer(gt.Layer1D(bottom=-7., soilname="zand_171"))
    assert g.num_layers()==3

    #add an invalid layer
    g.add_layer(gt.Layer1D(bottom=-6., soilname="zand_17"))
    assert g.num_layers()==3
    
    g.print_layers()
