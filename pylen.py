import os
import re
from gcode import Gcode

class Layer:
    """
    Helper class for accounting layers
    """
    def __init(self, color='',slen=0,elen=0):
        self.color = color  #the layer color
        self.slen = slen    #the starting length for this layer
        self.elen = elen   #the end length for the this layer

class Pylen:
    """
    Class which opens marlin style gcode file and returns a list of layer lengths
    """
    def __init__(self,path=''):
        self.linecount = 0
        self.path = path
        self.gc   = Gcode(path)
