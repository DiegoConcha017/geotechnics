class CPT:
    def __init__(self):
        """A CPT (cone penetration test) contains information on subsoil parameters."""
        self.xy = [] #location in RD coordinates
        self.surfacelevel = 0.0 #surfacelevel of the cpt
        self.z = [] #values of depths
        self.qc = [] #values of cone resistance
        self.pw = [] #values of plaatselijke wrijving
        self.wg = [] #values of wrijvingsgetal
        self.uu = [] #values of waterspanning
        self.preex = 0.0 #amount of pre excavation
        self.testid = "No name"

    def read(self, filename):
        """Load CPT from GEF file"""
        lines = open(filename,  'r').readlines()
        columnseperator, columninfo, columnvoid, index = self._read_header(lines)
        self._read_data(lines, index, columnseperator, columninfo, columnvoid)

    def _read_header(self, lines):
        """Read the first part of the CPT which is a header containing metadata"""
        columninfo = []
        columnvoid = []
        columnseperator = ' '
        for i in range(0, len(lines)):
            if lines[i].find("#EOH")>-1:
                return columnseperator, columninfo, columnvoid, i+1

            id, argsline = lines[i].split('=')
            args = [a.strip() for a in argsline.split(',')] #strip all whitespaces front and rear

            if id=="#COLUMNINFO":
                columninfo.append([int(args[0]), int(args[3])])
            elif id=="#COLUMNSEPARATOR":
                columnseperator = args[1]
            elif id=="#COLUMNVOID":
                columnvoid.append(int(float(args[1])))
            elif id=="#XYID":
                self.xy = [float(args[1]), float(args[2])]
            elif id=="#ZID":
                self.surfacelevel = float(args[1])
            elif id=="#TESTID":
                self.testid = args[0]
            elif id=="#MEASUREMENTVAR" and int(args[0]) == 13:
                self.preex = float(args[1])

    def _read_data(self, lines, index, columnseperator, columninfo, columvoid):
        """Read the second part of the CPT which contains the measurement"""
        #determine the location of the columns with the needed data
        iz, iqc, ipw, iwg = -1, -1, -1, -1
        for c in columninfo:
            if c[1] == 1: #sondeerlengte
                iz = c[0] - 1 #zero based indexing
            elif c[1] == 2: #punt druk
                iqc = c[0] - 1
            elif c[1] == 3: #lokale wrijving
                ipw = c[0] - 1
            elif c[1] == 4: #wrijvings getal
                iwg = c[0] - 1
            elif c[1] == 11: #gec. diepte (maatgevend over sondeerlengte)
                iz = c[0] - 1

        #read and save data
        for i in range(index, len(lines)):
            args = [a.strip() for a in lines[i].split(columnseperator)]

            #make sure the line does not contain any columnvoid value, cpt will skip this incomplete data
            skip = False
            if len(columvoid)>0:
                skip = float(args[iqc]) == columvoid[iqc]
                skip = skip or float(args[iz]) == columvoid[iz]
                skip = skip or float(args[ipw]) == columvoid[ipw]
                if iwg > -1:
                    skip = skip or float(args[iwg]) == columvoid[iwg]

            if not skip:
                qc = float(args[iqc])
                if qc <= 0.0: qc = 1e-5
                pw = float(args[ipw])
                if pw < 1e-5: pw = 1e-5
                self.qc.append(qc)
                self.z.append(self.surfacelevel - self.preex - abs(float(args[iz])))
                self.pw.append(pw)
                if iwg > 0:
                    wg = float(args[iwg])
                    if wg < 0.0: wg = 0.0
                    self.wg.append(wg)
                else:
                    self.wg.append(pw/qc * 100.0)

    def plot(self, exportpath=""):
        """Plot the CPT using matplotlib
        exportpath = path to export the plot to."""
        import matplotlib.pyplot as plt
        from matplotlib import gridspec
        from matplotlib import rc
        import os.path

        font = {'size': 8}
        rc('font', **font)
        plt.close('all')
        fig = plt.figure(figsize=(10,6))
        gs = gridspec.GridSpec(1, 3, width_ratios=[3, 1, 1])
        qcplot = fig.add_subplot(gs[0])
        qcplot.set_xlim([0,30])
        qcplot.set_title("conusweerstand [MPa]")
        qcplot.plot(self.qc, self.z)
        pwplot = fig.add_subplot(gs[1])
        pwplot.set_xlim([0,0.2])
        pwplot.set_title("plaatselijke wrijving [MPa]")
        pwplot.plot(self.pw, self.z)
        wgplot = fig.add_subplot(gs[2])
        wgplot.set_xlim([0,10])
        wgplot.set_title("wrijvingsgetal [%]")
        wgplot.plot(self.wg, self.z)
        gs.tight_layout(fig)
        plt.suptitle(self.testid)
        if exportpath!="":
            filename = os.path.join(exportpath, self.testid + ".png")
            plt.savefig(filename)
        else:
            plt.show()

    def to_geometry1d(self):
        """Convert the cpt to a Geometry1D object"""
        pass
