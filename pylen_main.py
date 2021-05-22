from PyQt5 import QtGui, QtWidgets
from PyQt5.Qt import Qt
from pylen_ui import Ui_MainWindow
from pylen_clen_ui import Ui_CutLengthWorkSheet
from pylen import Pylen
import matplotlib.pyplot as plt
import numpy as np
import os
from pylen_worker import *
from settings import Settings


class SegmentFrame(object):
    def __init__(self,parent,SegmentName="SegmentName",SegmentLayer=0,SegmentLayerMax=9999,SegmentUpdateCallBack=None):
        self.segment_name    = SegmentName
        self.segment_layer   = SegmentLayer
        self.segment_layer_max = SegmentLayerMax
        self.segment_color = QtGui.QColor("#f0f0f0")
        self.frame = QtWidgets.QFrame(parent)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.frame)
        self.spinBox.setMaximum(self.segment_layer_max)
        self.spinBox.setValue(self.segment_layer)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setToolTip("Set the last layer for this segment")
        self.horizontalLayout.addWidget(self.spinBox)
        self.pushButtonSegment = QtWidgets.QPushButton(self.frame)
        self.pushButtonSegment.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButtonSegment)
        self.label.setText(self.segment_name)
        self.pushButtonSegment.setText("SetColor")
        self.pushButtonSegment.setToolTip("Set the color for this segment")

        self.pushButtonSegment.setStyleSheet(f"background-color:{self.segment_color.name()}")
        self.pushButtonSegment.clicked.connect(self.setColor)
        self.spinBox.valueChanged.connect(self.spinBoxOnChange)
        self.update_callback = SegmentUpdateCallBack

    def setColor(self):
        self.segment_color  = QtWidgets.QColorDialog.getColor()
        self.pushButtonSegment.setStyleSheet(f"background-color:{self.segment_color.name()}")
        print(f"Segment{self.segment_name} color set to {self.segment_color.name()}")
        self.update()

    def spinBoxOnChange(self):
        self.segment_layer = self.spinBox.value()
        print(f"Segment{self.segment_name} spinbox changed to {self.spinBox.value()}")
        self.update()

    def update(self):
        if self.update_callback is not None:
           self.update_callback(self)

    def setLayer(self,layer):
        self.segment_layer = layer
        self.spinBox.setValue(layer)

    def __str__(self):
        return f'name:{self.segment_name} layer:{self.segment_layer} color:{self.segment_color.name()}'


class Pylen_Clen_UI(Ui_CutLengthWorkSheet):
        def __init__(self, pl):
            super().__init__()
            self.form = QtWidgets.QWidget()
            self.setupUi(self.form)
            self.pl = pl
            self.layer_count   = int(self.pl.gc.d["LAYER_COUNT"])
            self.layer_list = []
            self.color_list = []
            self.length_list = []
            self.pos_list    = []
            self.start_up_filament = self.pl.gc.start_eabs
            self.layer_data  = self.pl.gc.edata
            self.segment_count = 1
            self.scene = QtWidgets.QGraphicsScene()
            self.greenBrush = QtGui.QBrush(Qt.green)
            self.grayBrush = QtGui.QBrush(Qt.gray)
            self.pen = QtGui.QPen(Qt.red)
            self.pushButton_AddSegment.setToolTip("Adds a new segment")
            self.graphicsView.setScene(self.scene)
            self.graphicsView.setToolTip("Segments shown here go from left to right. The leftmost segment is the end which goes into the printer first. Startup filament is Not included in first segment.")
            self.pushButton_AddSegment.clicked.connect(self.add_segment)
            self.sf_list = []
            self.sceneLengthTextItem_list = []
            self.form.show()

        def add_segment(self):
            sf = SegmentFrame(self.scrollAreaWidgetContents, SegmentName=f"Segment {self.segment_count} up to Layer:",
                              SegmentLayer=self.layer_count, SegmentLayerMax=self.layer_count,
                              SegmentUpdateCallBack=self.segment_updated)

            if self.segment_count == 1:
                pass
            elif self.segment_count == 2:
                l = int(self.sf_list[-1].segment_layer / 2)
                self.sf_list[-1].setLayer(self.layer_count-l)
            else:
                l = int((self.layer_count - self.sf_list[-2].segment_layer) / 2)
                self.sf_list[-1].setLayer(self.layer_count-l)

            self.sf_list.append(sf)
            self.verticalLayout.addWidget(sf.frame)
            self.segment_count += 1
            self.update_lists()
            self.update_scene()

        def update_lists(self):
            self.layer_list  = []
            self.color_list  = []
            self.length_list = []
            self.pos_list    = []

            for s in self.sf_list:
                self.layer_list.append(s.segment_layer)
                self.color_list.append(s.segment_color.name())

            for nn in range(len(self.layer_list)):

                if nn == 0:
                    ll  = self.layer_list[nn]
                    pos = self.layer_data[ll-1]
                    self.length_list.append(pos)
                    self.pos_list.append(pos)
                else:
                    ll = self.layer_list[nn]
                    mm = self.layer_list[nn-1]
                    pos = self.layer_data[ll-1]
                    self.length_list.append(self.layer_data[ll-1] - self.layer_data[mm-1])
                    self.pos_list.append(pos)

        def update_scene(self):
            x0 = self.graphicsView.width() * 0.1
            y0 = self.graphicsView.height()/2
            row_text_height = 20
            total_length = self.layer_data[-1]
            gv_pixels_width = self.graphicsView.width() * 0.8
            pix_factor      = gv_pixels_width / total_length
            self.scene.clear()
            self.sceneLengthTextItem_list = []
            textItem = self.scene.addText("Units[mm]")
            textItem.setPos(x0, y0 + row_text_height * 1 )
            self.sceneLengthTextItem_list.append(textItem)
            textItem = self.scene.addText(f"Layer Count[-]:{self.layer_count}")
            textItem.setPos(x0, y0 + row_text_height * 2)
            self.sceneLengthTextItem_list.append(textItem)
            textItem = self.scene.addText(f"Total filament[mm]:{self.layer_data[-1]:.1f}")
            textItem.setPos(x0, y0 + row_text_height * 3)
            self.sceneLengthTextItem_list.append(textItem)
            startup_str = f"Startup filament[mm]:{self.start_up_filament:.1f} - Not included in first segment"
            textItem = self.scene.addText(startup_str)
            textItem.setPos(x0, y0 + row_text_height * 4)
            self.sceneLengthTextItem_list.append(textItem)

            #draw the startup line
            color = QtGui.QColor(self.color_list[0])
            pen = QtGui.QPen(color)
            pen.setWidth(5)
            y = y0 + row_text_height * 4.5
            x1 = x0 + textItem.boundingRect().width() * 1.1
            x2 = x1 + self.start_up_filament

            self.scene.addLine(x1, y, x2, y, pen)

            #draw the segment lines
            for nn in range(len(self.length_list)):
                color = QtGui.QColor(self.color_list[nn])
                pen   = QtGui.QPen(color)
                pen.setWidth(5)
                if nn == 0:
                    x1 = x0
                    y1 = y0
                    ll = self.layer_list[nn]
                    x2 = self.layer_data[ll-1] * pix_factor + x0
                    y2 = y0
                    self.scene.addLine(x1, y1, x2, y2, pen)
                    textItem = self.scene.addText(f"{self.length_list[nn]:.1f}")
                    textItem.setPos((x2+x1) / 2, y2 + 10)
                    self.sceneLengthTextItem_list.append(textItem)
                else:
                    ll = self.layer_list[nn]
                    mm = self.layer_list[nn-1]
                    x2 = self.layer_data[ll-1]*pix_factor + x0
                    y2 = y0
                    x1 = self.layer_data[mm-1]*pix_factor + x0
                    y1 = y0
                    self.scene.addLine(x1, y1, x2, y2, pen)
                    textItem = self.scene.addText(f"{self.length_list[nn]:.1f}")
                    textItem.setPos((x2+x1) / 2, y2 + 10)
                    self.sceneLengthTextItem_list.append(textItem)



        def get_segment_color_as_list(self):
            sc = []
            for s in self.sf_list:
                sc.append(s.segment_color.name())
            return sc

        def segment_updated(self, sf):
            if isinstance(sf, SegmentFrame):
                self.update_lists()
                self.update_scene()
                print(f'segment updated called for for {sf}')
                print(f'total number of segments:{len(self.sf_list)}')
                print(f'layer list:{self.layer_list}')
                print(f'color list:{self.color_list}')
                print(f'length list:{self.length_list}')
                print(f'pos list:{self.pos_list}')

class Pylen_UI(Ui_MainWindow):
    """
    Main UI window
    UI Generated using QT Designer
        UI_MainWindow derived from pylen_ui.ui
        pylen_ui.ui is generated by QTDesiger application
        to generate pylen_ui.py execute from terminal:
        >pyuic5 -xo pylen_ui.py pylen_ui.ui
    """
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.filename_report = self.settings.last_report_file
        self.filename_gcode  = self.settings.last_gcode_file
        self.pl = None
        self.threadpool = QtCore.QThreadPool()
        self.parse_completed = False
        self.parse_in_progress = False


    def pylen_setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.setupUi(MainWindow)
        self.pushButton_Generate.clicked.connect(self.pushButtonGenerateClicked)
        self.pushButton_OpenReport.clicked.connect(self.pushButtonOpenReporteClicked)
        self.actionOpen.triggered.connect(self.actionFileOpenTrigger)
        self.actionHelp.triggered.connect(self.actionFileHelpTrigger)
        self.actionAbout.triggered.connect(self.actionFileAboutTrigger)
        self.textBrowser_OutputWindow.setText('Use File->Open to select GCode and then Click Generate Button.')
        self.progressBar.setProperty("value", 0)
        self.lineEdit_ReportPath.setText(self.filename_report)
        self.lineEdit_GCodePath.setText(self.filename_gcode)

    def pushButtonOpenReporteClicked(self):
        if self.filename_report is not None and os.path.exists(self.filename_report) is True:
            os.system(self.filename_report)
        else:
            msgBox = QtWidgets.QMessageBox()
            msgBoxTxt = """
                                <html><head/>
                                <body>
                                <p>No report exists</p>
                                </body>
                                </html>
                                """
            msgBox.setWindowTitle("Generate Message No GCode File Set")
            msgBox.setText(msgBoxTxt)
            msgBox.exec_()

    def actionFileOpenTrigger(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, "QFileDialog.getOpenFileName()",
                                                            os.path.dirname(self.settings.last_gcode_file),
                                                  "GCode Files (*.gcode);;All Files (*)", options=options)
        if fileName:
            basename = os.path.basename(fileName)
            dirname  = os.path.dirname(fileName)
            basename_ = basename.split('.')
            self.filename_gcode = os.path.join(dirname, basename)
            self.settings.last_gcode_file = self.filename_gcode
            self.filename_report = os.path.join(dirname, f"{basename_[0]}.csv")
            self.settings.last_report_file = self.filename_report
            self.lineEdit_GCodePath.setText(self.filename_gcode)
            self.lineEdit_ReportPath.setText(self.filename_report)
            self.parse_completed = False
            self.progressBar.setProperty("value", 0)

    def actionFileHelpTrigger(self):
        msgBox = QtWidgets.QMessageBox()
        msgBoxTxt = """
        <html><head/>
        <body><p>Pylen Help:</p>
        <p>Program Purpose:</p>
        <p>Read 3DPrinter Gcode and extract filament usage per layer.
        The filamanent usage is the cumulative filament used at the &quot;END&quot; of each layer.
        </p>
        <p/>Uses:
        <p/>-Estimate filament used per layer
        <p/>-Plan layer color usage for multi color printing
        <p>File-&gt;Open</p>
        <p>Sets the path to the gcode file to be read. The default behavior is to set the report output path as the gcode_file.csv</p>
        <p>Report File Path</p><p>The path where pylen generates its report information as a .csv format which can be opened in a spreadsheet program</p><p>Generate:</p>
        <p>After the gcode path has been set using the File-&gt;Open action. Click on the Generate Button to create a usage report and display a usage graph</p>
        <p>Notes:</p>
        <p>Tested using Cura withe Ender 3 profile / Marlin flavor gcode!</p>
        <p>Send sample gcode for your printer to b.moniey@gmail.com to help add new flavors</p>
        </body></html>
        """
        msgBox.setWindowTitle("Pylen Help Window")
        msgBox.setText(msgBoxTxt)
        msgBox.exec_()


    def actionFileAboutTrigger(self):
        msgBox = QtWidgets.QMessageBox()
        msgBoxTxt = """
        <html><head/>
        <body>
        <p>Pylen Filament Usage Generator</p>
        <p>Version: 1.1.1</p>
        <p>Release Date: May 22, 2021</p>
        <p>Written by: Brian Moran</p>
        <p>Email: b.moniey@gmail.com</p>
        </body>
        </html>
        """
        msgBox.setWindowTitle("Pylen About Window")
        msgBox.setText(msgBoxTxt)
        msgBox.exec_()

    def makePlot(self):
        l = np.arange(1, int(self.pl.gc.d["LAYER_COUNT"])+1, 1)
        fig, ax = plt.subplots()
        ax.plot(l, self.pl.gc.edata, 'ro')
        plt.grid(True)
        ax.set(xlabel='Layer',
               ylabel='Filament Length Usage[mm]',
               title=f'file:{self.filename_gcode}')

        for n in l:
            label = f'({n},{self.pl.gc.edata[n-1]:.0f})'
            plt.annotate(label,
                         (n, self.pl.gc.edata[n-1]),
                         textcoords="offset points",
                         xytext=(30, -10),
                         ha='center')

        plt.show()

    def makeCSV(self):
        csv = [f'Start up Filament Usage[mm]:{self.pl.gc.start_eabs:.2f}']
        csv.append('N,length[mm]')
        for n in range(int(self.pl.gc.d["LAYER_COUNT"])):
            csv.append(f'{n + 1},{self.pl.gc.edata[n]:.0f}')
        return csv

    def makeCSVFile(self):
        fd = open(self.filename_report,'w')
        fd.write(f'gcode file:,{self.filename_gcode}\n')
        fd.write(f'Layer Count:,{self.pl.gc.d["LAYER_COUNT"]}\n')
        fd.write(f'Total Filament[mm]:,{float( self.pl.gc.d["Filament used"] ) * 1000.0:.1f}\n')
        fd.write(f'GCode Flavor:,{self.pl.gc.d["FLAVOR"]}\n')
        fd.write(f'Start up Filament Usage[mm],{self.pl.gc.start_eabs:.2f}\n')
        fd.write('Layer[-],length[mm]\n')
        for n in range(int(self.pl.gc.d["LAYER_COUNT"])):
            fd.write(f'{n + 1},{self.pl.gc.edata[n]:.0f}\n')
        fd.close()

    def update_progress(self):
        prog = self.pl.gc.progress()
        self.progressBar.setProperty("value", prog)

    def thread_complete(self):
        self.parse_completed = True


    def pushButtonGenerateClicked(self):
        if self.filename_gcode is not None and self.parse_in_progress is False:
            self.textBrowser_OutputWindow.setText('File Open, Starting a new session. Waiting for Generate to Start:')
            self.textBrowser_OutputWindow.append(f'GCode File Path Set to:{self.filename_gcode}')
            self.textBrowser_OutputWindow.append(f'GCode Report Path Set to:{self.filename_gcode}')
            self.textBrowser_OutputWindow.append('Reading GCode. This may take a moment...')
            #move the parsing to a worker thread

            self.pl = Pylen(self.filename_gcode)
           #self.pl.gc.parse()
            self.parse_completed = False
            self.parse_in_progress = True
            worker = Worker(self.pl.gc.parse)  # Any other args, kwargs are passed to the run function
            #worker.signals.result.connect(self.print_output)
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.update_progress)

            # Execute
            self.threadpool.start(worker)
            while self.parse_completed is False:
                QtGui.QGuiApplication.processEvents()

            self.textBrowser_OutputWindow.append('Finished reading GCode')
            self.textBrowser_OutputWindow.append(f'total filament used:{self.pl.gc.eabs:.1f}[mm]')
            delta = float(self.pl.gc.d["Filament used"]) * 1000 -self.pl.gc.eabs
            if delta < 1:
                self.textBrowser_OutputWindow.append('Stated vs Calculated filament usage: < 1mm')
            else:
                self.textBrowser_OutputWindow.append(f'Stated vs Calculated filament usage:{delta:.1f}')
            self.textBrowser_OutputWindow.append(f'layer report for file:{self.filename_gcode}')
            self.textBrowser_OutputWindow.append(f'layer count:{int(self.pl.gc.d["LAYER_COUNT"])}')
            #csv = self.makeCSV()
            #for line in csv:
            #    self.textBrowser_OutputWindow.append(line)
            self.textBrowser_OutputWindow.append(f'generating csv file:{self.filename_report}')
            self.makeCSVFile()

            self.textBrowser_OutputWindow.append(f'generating plot')
            self.makePlot()
            self.textBrowser_OutputWindow.append(f'Done')
            self.parse_in_progress = False
            self.clen_ui = Pylen_Clen_UI(self.pl)


        else:
            msgBox = QtWidgets.QMessageBox()
            msgBoxTxt = """
                    <html><head/>
                    <body>
                    <p>Use File Open to select GCode path or type in manually</p>
                    </body>
                    </html>
                    """
            msgBox.setWindowTitle("Generate Message No GCode File Set")
            msgBox.setText(msgBoxTxt)
            msgBox.exec_()

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    with Settings() as settings:
        ui = Pylen_UI(settings)
        ui.pylen_setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()