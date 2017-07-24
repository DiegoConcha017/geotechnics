from soiltype import Soiltype

class SoilLib:
    def __init__(self):
        self.soils = []

    def add_soiltype(self, name, ydry, ysat):
        self.soils.append(Soiltype(name, ydry, ysat))

    def get_by_name(self, name):
        for soil in self.soils:
            if soil.name == name:
                return soil
        return None
