def test_cpt():
    import geotechnics as gt
    cpt = gt.cpt.CPT()
    cpt.read('data/b_cpt.gef')
    cpt.plot()

if __name__=="__main__":
    test_cpt()
