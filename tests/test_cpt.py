def test_cpt():
    import geotechnics as gt
    cpt = gt.cpt.CPT()
    cpt.read('tests/data/a_cpt.gef')
    cpt.read('tests/data/b_cpt.gef')
    cpt.plot()

if __name__=="__main__":
    test_cpt()
