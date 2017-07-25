import copy

class Geometry1D:
    def __init__(self, soillib=None):
        """Init a Geometry1D object"""
        self._layers = []
        self._soillib = soillib

    def _merge_layers(self):
        """This function merges two or more consecutive layers with the same soilname to one layer"""
        oldlayers = copy.deepcopy(self._layers)
        self._layers = []
        self._layers.append(oldlayers[0])
        for i in range(1, len(oldlayers)):
            if oldlayers[i].soilname == self._layers[-1].soilname:
                self._layers[-1].bottom = oldlayers[i].bottom
            else:
                self._layers.append(oldlayers[i])

    def add_layer(self, layer1d):
        """Add a new layer, if it is not the first layer the top of the layer is ignored and just stacked under the previous layer"""
        if self.num_layers() > 0:
            if self._soillib.get_by_name(layer1d.soilname) == None:
                print("[ERROR] Geometry1D.add_layer: Unknown soilname %s" % layer1d.soilname)
                return
            if self._layers[-1].bottom < layer1d.bottom:
                print("[ERROR] Geometry1D.add_layer: New layer bottom %.2f is higher than the bottom of the layer on top %.2f" % (layer1d.bottom, self._layers[-1].bottom))
                return
            layer1d.top = self._layers[-1].bottom
            self._layers.append(layer1d)
        else:
            self._layers.append(layer1d)

    def insert_layer(self, layer1d):
        """Insert a layer anywhere, just be sure that the top and the bottom do not exceed the previous top and bottom of the entire geometry"""
        if self.num_layers() > 0:
            if self._soillib.get_by_name(layer1d.soilname) == None:
                print("[ERROR] Geometry1D.insert_layer: Unknown soilname %s" % layer1d.soilname)
                return
            if layer1d.top >= self._layers[0].top:
                print("[ERROR] Geometry1D.insert_layer: Top of new inserted %.2 is higher than highest layer %.2f" % (layer1d.top, self._layers[0].top))
                return
            if layer1d.bottom <= self._layers[-1].bottom:
                print("[ERROR] Geometry1D.insert_layer: Bottom of inserted layer %.2 is higher than lowest layer %.2f" % (layer1d.top, self._layers[-1].bottom))
                return

            layeridx_top = -1
            layeridx_bottom = -1
            for i in range(0, len(self._layers)):
                if self._layers[i].top > layer1d.top and layer1d.top >= self._layers[i].bottom:
                    layeridx_top = i
                if self._layers[i].top > layer1d.bottom and layer1d.bottom >= self._layers[i].bottom:
                    layeridx_bottom = i


            newlayers = []
            for i in range(0, len(self._layers)):
                if i==layeridx_top:
                    newlayers.append(copy.deepcopy(self._layers[i]))
                    newlayers[-1].bottom = layer1d.top
                    if i==layeridx_bottom: #insert layer
                        newlayers.append(layer1d)
                        if newlayers[-1].bottom > self._layers[i].bottom:
                            newlayers.append(copy.deepcopy(self._layers[i]))
                            newlayers[-1].top = layer1d.bottom
                    else:
                        newlayers.append(layer1d)

                elif i==layeridx_bottom:
                    if not layeridx_top==layeridx_bottom:
                        newlayers.append(copy.deepcopy(self._layers[i]))
                        newlayers[-1].top = layer1d.bottom
                elif self._layers[i].bottom < layer1d.bottom:
                    newlayers.append(copy.deepcopy(self._layers[i]))

            self._layers = []
            for n in newlayers:
                self._layers.append(n)

            self._merge_layers()
        else:
            print("[ERROR] Geometry1D.insert_layer: Geometry1D does not have a first layer, initialize first with the top layer")




    def delete_layer(self, layer1d):
        """TODO"""
        pass

    def from_cpt(self, cptfile, method="CUR"):
        """TODO"""
        pass

    def plot(self):
        """TODO"""
        pass

    def print_layers(self):
        """Print a description of the geometry"""
        print("%-20s%10s%10s" % ("soilname","top","bottom"))
        for layer in self._layers:
            print("%-20s%10.2f%10.2f" % (layer.soilname, layer.top, layer.bottom))

    def num_layers(self):
        """Return the number of layers"""
        return len(self._layers)
