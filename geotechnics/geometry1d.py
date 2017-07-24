class Geometry1D:
    def __init__(self, soillib=None):
        self._layers = []
        self._soillib = soillib

        self._is_initialized = False

    def init_layers(self, layer1d):
        if not self._is_initialized:
            self._layers.append(layer1d)
            self._is_initialized = True
        else:
            print("Geometry1D already contains layers, clear first before initialing again.")

    def add_layer(self, layer1d):
        if self._is_initialized:
            if self._soillib.get_by_name(layer1d.soilname) == None:
                print("[ERROR] Geometry1D.add_layer: Unknown soilname %s" % layer1d.soilname)
                return
            if self._layers[-1].bottom < layer1d.bottom:
                print("[ERROR] Geometry1D.add_layer: New layer bottom %.2f is higher than the bottom of the layer on top %.2f" % (layer1d.bottom, self._layers[-1].bottom))
                return
            layer1d.top = self._layers[-1].bottom
            self._layers.append(layer1d)
        else:
            print("Geometry1D does not have a first layer, initialize first with the top layer")

    def insert_layer(self, top, layer1d):
        pass

    def delete_layer(self, layer1d):
        pass

    def from_cpt(self, cptfile, method="CUR"):
        pass

    def plot(self):
        pass

    def print_layers(self):
        print "%-20s%10s%10s" % ("soilname","top","bottom")
        for layer in self._layers:
            print "%-20s%10.2f%10.2f" % (layer.soilname, layer.top, layer.bottom)

    def num_layers(self):
        return len(self._layers)
