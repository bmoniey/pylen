class PylenUnit(object):
    """
    simple units class to handle a couple cases
    intent is to take care of mm,M and inches
    assumes mm are always given to covert
    all internal calculations us mm as the basis
    """
    IDX_MM = 0
    IDX_M = 1
    IDX_INCH = 2

    LONG_STRING = {IDX_MM: "Milli-Meter", IDX_M: "Meter", IDX_INCH: "Inch"}
    SHORT_STRING = {IDX_MM: "mm", IDX_M: "m", IDX_INCH: "in"}
    CONVERT_TO_MM = {IDX_MM: 1.0, IDX_M: 1000.0, IDX_INCH: 25.4}
    FORMAT = {IDX_MM: '.0f', IDX_M: '.3f', IDX_INCH: '.1f'}

    def __init__(self, val, idx=IDX_MM):
        """
        val the value in the units according to the idx
        idx the type or index see indexes from base class definition
        val_mm the internal value as mm
        """
        self.val = float(val)
        self.idx = int(idx)
        self.val_mm = val * PylenUnit.CONVERT_TO_MM[self.idx]

    def setUnit(self, idx=IDX_MM):
        self.idx = int(idx)

    def unitStr(self):
        return PylenUnit.SHORT_STRING[self.idx]

    def __str__(self):
        return f'{self.convert()} {PylenUnit.SHORT_STRING[self.idx]}'

    def lStr(self):
        return f'{self.val} {PylenUnit.LONG_STRING[self.idx]}'

    def convert(self):
        return self.val_mm / PylenUnit.CONVERT_TO_MM[self.idx]

    def __add__(self, other):
        if type(other) is type(self):
            return PylenUnit(self.val_mm + other.val_mm)

    def __mul__(self, other):
        if type(other) is type(self):
            return PylenUnit(self.val_mm * other.val_mm)

    def __sub__(self, other):
        if type(other) is type(self):
            return PylenUnit(self.val_mm - other.val_mm)

    def __truediv__(self, other):
        if type(other) is type(self):
            if other.val_mm != 0.0:
                return PylenUnit(self.val_mm / other.val_mm)


if __name__ == "__main__":
    print('PylenUnit examples...')
    print('Creating pu as 100 mm')
    pu1 = PylenUnit(100, PylenUnit.IDX_MM)
    print(f"PylenUnit as {pu1}")
    pu1.setUnit(PylenUnit.IDX_MM)
    print(f"PylenUnit as {pu1}")
    pu1.setUnit(PylenUnit.IDX_M)
    print(f"PylenUnit as {pu1}")
    pu1.setUnit(PylenUnit.IDX_INCH)
    print(f"PylenUnit as {pu1}")

    print('Creating pu as 100 inches')
    pu1 = PylenUnit(100, PylenUnit.IDX_INCH)
    print(f"PylenUnit as {pu1}")
    pu1.setUnit(PylenUnit.IDX_MM)
    print(f"PylenUnit as {pu1}")
    pu1.setUnit(PylenUnit.IDX_M)
    print(f"PylenUnit as {pu1}")
    pu1.setUnit(PylenUnit.IDX_INCH)
    print(f"PylenUnit as {pu1}")
