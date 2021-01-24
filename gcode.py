import os
import re
import numpy as np

class Layer:
    def __init__(self,number=0,estart=0):
        """
        A clase to hold layer data
        :param number: The layer number
        :param estart: the starting extruder length
        """
        self.number = number
        self.e      = 0
        self.efirst = -1

    def ereset(self, reset_val):
        self.efirst = float(reset_val)

    def eupdate(self,E_VALUE):
        """
        update the layer exrude length
        :param E_VALUE:
        :return:
        """
        if self.efirst == -1:
            self.ereset(E_VALUE)
        else:
            self.e += float(E_VALUE) - self.efirst


class Gcode:
    """
    This class will open and read gcode files
    """
    def __init__(self, path=''):
        self.linecount = 0
        self.path = path
        self.f    = self.open()
        self.d    = {}
        self.d["LAYER_LIST"]=[]
        self.d["LAYER_COUNT"]=0
        self.d["E"]=0
        self.current_layer = None
        self.e0 = 0
        self.e1 = 0
        self.eabs  = 0
        self.edata = None
        self.start_gcode = False
        self.start_e0 = 0
        self.start_e1 = 0
        self.start_eabs = 0

    def open(self):
        pattern = re.compile(".*\.gcode$")
        pattern.match(self.path)
        if os.path.exists(self.path):
            if pattern.match(self.path):
                f = open(self.path, "r")
                return f
            else:
                print(f'{self.path} is not a .gcode file')
                return None
        else:
            print(f'{self.path} does not exist')
            return None

    def eupdate(self, e=None):
        """
        update the etruder position with a new entry
        :param e:
        :return:
        """
        if e is not None:
            ef = float(e)
            if ef > self.e0:
                self.e1 = self.e0
                self.e0 = ef
                self.eabs += self.e0 - self.e1

                if self.current_layer != None and self.edata is not None:
                    self.edata[int(self.current_layer.number)] = self.eabs
            elif ef == 0:
                self.e1 = 0
                self.e0 = 0
            else:
                pass

    def progress(self):
        if int(self.d["LAYER_COUNT"]) > 0:
            return int( 100.0 * (float(self.current_layer.number) + 1.0 ) / float( self.d["LAYER_COUNT"] ))
        else:
            return 0

    def parse(self,progress_callback):
        for ln in self.f:
            self.linecount +=1
            patterns = []
            #;FLAVOR: Marlin
            patterns.append(re.compile(";(FLAVOR):(.*)"))
            #;TIME:6721
            patterns.append(re.compile(";(TIME):(\d*)"))
            #;Filament used: 5.51279m
            patterns.append(re.compile(";(Filament used):\s*(\d*\.*\d*)m*"))
            #;Layer height: 0.2
            patterns.append(re.compile(";(Layer height):\s*(\d*\.*\d*)"))
            #;MINX:57.185
            patterns.append(re.compile(";(MINX):\s*(\d*\.*\d*)"))
            #;MINY:70.157
            patterns.append(re.compile(";(MINY):\s*(\d*\.*\d*)"))
            #;MINZ:0.2
            patterns.append(re.compile(";(MINZ):\s*(\d*\.*\d*)"))
            #;MAXX:177.831
            patterns.append(re.compile(";(MAXX):\s*(\d*\.*\d*)"))
            #;MAXY: 128.472
            patterns.append(re.compile(";(MAXY):\s*(\d*\.*\d*)"))
            #;MAXZ: 10
            patterns.append(re.compile(";(MAXZ):\s*(\d*\.*\d*)"))
            #;LAYER_COUNT: 50
            patterns.append(re.compile(";(LAYER_COUNT):\s*(\d*\.*\d*)"))
            #;LAYER:0
            patterns.append(re.compile(";(LAYER):\s*(\d*)"))
            #G(number)
            patterns.append(re.compile("\s*(G)(\d+)(.*)"))
            #M(number)
            patterns.append(re.compile("\s*(M)(\d+)(.*)"))
            #; Ender 3 Custom Start G-code
            patterns.append(re.compile(";\s*Ender 3 Custom (Start G-code)"))
            # G1 F2700 E313.64266
            pg1a = re.compile("\s*F(\d+) E(\d+\.*\d*)")
            # G1 F600 X156.051 Y84.775 E274.24112
            pg1b = re.compile("\s*F(\d+)\s*X(\d+\.*\d*)\s*Y(\d+\.*\d*)\s*E(\d+\.*\d*)")
            # G1 X65.343 Y76.759 E30.31173
            pg1c = re.compile("\s*X(\d+\.*\d*)\s*Y(\d+\.*\d*)\s*E(\d+\.*\d*)")
            #G1 X0.1 Y200.0 Z0.3 F1500.0 E15 ; Draw the first line
            pg1s = re.compile("\s*X(\d+\.*\d*)\s*Y(\d+\.*\d*)\s*Z(\d+\.*\d*)\s*F(\d+\.*\d*)\s*E(\d+\.*\d*).*")

            for p in patterns:
                m = p.match(ln)
                if m:
                    g = m.group(1)
                    if g == "G":
                        if m.group(2) == "1":
                            pg1am = pg1a.match(m.group(3))
                            if pg1am:
                                self.current_layer.eupdate(pg1am.group(2))
                                self.d["E"] = pg1am.group(2)
                                self.eupdate(self.d["E"])
                                break

                            pg1bm = pg1b.match(m.group(3))
                            if pg1bm:
                                self.current_layer.eupdate(pg1bm.group(4))
                                self.d["E"] = pg1bm.group(4)
                                self.eupdate(self.d["E"])
                                break

                            pg1cm = pg1c.match(m.group(3))
                            if pg1cm:
                                self.current_layer.eupdate(pg1cm.group(3))
                                self.d["E"] = pg1cm.group(3)
                                self.eupdate(self.d["E"])
                                break
                            pg1sm = pg1s.match(m.group(3))
                            if pg1sm:
                                if self.start_gcode:
                                    self.start_e1 = self.start_e0
                                    self.start_e0 = float(pg1sm.group(5))
                                    self.start_eabs += self.start_e0-self.start_e1
                                break
                        elif m.group(2) == "0":
                            pass
                        elif m.group(2) =="92":
                            lm = re.match("\s*E(\d+.*\d*)(.*)",m.group(3))
                            if lm:
                                print(f"Extruder Reset:{lm.group(1)}")
                                self.d["E"] = 0
                                self.eupdate(self.d["E"])
                        elif m.group(2) == "1":
                            #set position
                            pass
                            #print(f'G1 {m.group(2)}')
                        elif m.group(2) == "0":
                            pass
                            #print(f'G0 {m.group(2)}')
                        elif m.group(2) == "91":
                            pass
                        elif m.group(2) == "90":
                            pass
                    elif g == "M":
                        if m.group(2) == "107":
                            print("M107 Fan Off")
                        if m.group(2) == "106":
                            lm = re.match("\s*S(\d+)",m.group(3))
                            if lm:
                                print(f"M106 Set Fan Speed:{lm.group(1)}")
                    elif g=="LAYER":
                        self.d["LAYER"]=m.group(2)
                        print(f'LAYER:{self.d["LAYER"]}')
                        self.current_layer  = Layer(self.d["LAYER"],self.d["E"])
                        print(f'New Layer:{self.d["LAYER"]} E:{self.d["E"]}')
                        self.d["LAYER_LIST"].append(self.current_layer)
                        self.start_gcode = False
                        progress_callback.emit(self.progress())
                    elif g =="LAYER_COUNT":
                        self.d["LAYER_COUNT"] = int(m.group(2))
                        print(f'LAYER_COUNT:{self.d["LAYER_COUNT"]}')
                        self.edata = np.zeros(int(self.d["LAYER_COUNT"]))
                    elif g == "Start G-code":
                        print('Start G-code')
                        self.start_gcode = True
                    else:
                        self.d[m.group(1)]= m.group(2)
                        print(f'{m.group(1)}={m.group(2)}')

