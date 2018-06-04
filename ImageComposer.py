import sys
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint
from PyQt5.QtGui import  QImage, QPixmap, QPainter, QIcon
from PyQt5.QtWidgets import qApp, QApplication, QMainWindow, QWidget, QFileDialog,\
    QLabel, QPushButton, QToolButton, QComboBox,\
    QLayout, QGridLayout

resultSize = QSize(1200, 900)

def imagePos(q_image):
    return QPoint(
        (resultSize.width() - q_image.width())/2,
        (resultSize.height() - q_image.height()) / 2,
    )

class ImageComposer(QWidget):
    def __init__(self):
        super(ImageComposer, self).__init__()
        self._createCompents()
        self._createLayout()
        self._createSlot()
        self._default()

    def _createCompents(self):
        self.sourceBtn = QToolButton()
        self.sourceBtn.setIconSize(resultSize)

        self.destinationBtn = QToolButton()
        self.destinationBtn.setIconSize(resultSize)

        self.equalLabel = QLabel('=')


        self.resultLabel = QLabel()
        self.resultLabel.setMaximumWidth(resultSize.width())

        self.operatorComBox = QComboBox()
        self.operatorComBox.addItem('SourceOver', QPainter.CompositionMode_SourceOver)
        self.operatorComBox.addItem('DestinationOver', QPainter.CompositionMode_DestinationOver)
        self.operatorComBox.addItem('Clear', QPainter.CompositionMode_Clear)
        self.operatorComBox.addItem('Source', QPainter.CompositionMode_Source)
        self.operatorComBox.addItem('Destination', QPainter.CompositionMode_Destination)
        self.operatorComBox.addItem('SourceIn', QPainter.CompositionMode_SourceIn)
        self.operatorComBox.addItem('DestinationIn', QPainter.CompositionMode_DestinationIn)
        self.operatorComBox.addItem('SourceOut', QPainter.CompositionMode_SourceOut)
        self.operatorComBox.addItem('DestinationOut', QPainter.CompositionMode_DestinationOut)
        self.operatorComBox.addItem('SourceAtop', QPainter.CompositionMode_SourceAtop)
        self.operatorComBox.addItem('DestinationAtop', QPainter.CompositionMode_DestinationAtop)
        self.operatorComBox.addItem('Xor', QPainter.CompositionMode_Xor)
        self.operatorComBox.addItem('Plus', QPainter.CompositionMode_Plus)
        self.operatorComBox.addItem('Multiply', QPainter.CompositionMode_Multiply)
        self.operatorComBox.addItem('Screen', QPainter.CompositionMode_Screen)
        self.operatorComBox.addItem('Overlay', QPainter.CompositionMode_Overlay)
        self.operatorComBox.addItem('Darken', QPainter.CompositionMode_Darken)
        self.operatorComBox.addItem('Lighten', QPainter.CompositionMode_Lighten)
        self.operatorComBox.addItem('ColorDodge', QPainter.CompositionMode_ColorDodge)
        self.operatorComBox.addItem('ColorBurn', QPainter.CompositionMode_ColorBurn)
        self.operatorComBox.addItem('HardLight', QPainter.CompositionMode_HardLight)
        self.operatorComBox.addItem('SoftLight', QPainter.CompositionMode_SoftLight)
        self.operatorComBox.addItem('Difference', QPainter.CompositionMode_Difference)
        self.operatorComBox.addItem('Exclusion', QPainter.CompositionMode_Exclusion)

        # self.goBtn = QPushButton('GO!')

    def _createLayout(self):
        main_layout = QGridLayout()
        main_layout.addWidget(self.sourceBtn, 0, 0, 3, 1)
        main_layout.addWidget(self.operatorComBox, 1, 1)
        main_layout.addWidget(self.destinationBtn, 0, 2, 3, 1)
        main_layout.addWidget(self.equalLabel, 1, 3)
        # main_layout.addWidget(self.goBtn, 1, 3, 1, 1)
        main_layout.addWidget(self.resultLabel, 0, 4, 3, 1)
        main_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(main_layout)

    def _createSlot(self):
        self.sourceBtn.clicked.connect(self.chooseSource)
        self.destinationBtn.clicked.connect(self.chooseDestination)
        self.operatorComBox.activated.connect(self.recalculateResult)

    def _default(self):
        self.resultImage = QImage(resultSize, QImage.Format_ARGB32_Premultiplied)
        self.sourceImage = self._loadImage('images/cz.png',
                                           self.sourceBtn)
        self.destinationImage = self._loadImage('images/mask.png',
                                                self.destinationBtn)

    def _loadImage(self, file_name, tool_btn):
        image = QImage()
        image.load(file_name)
        fixed_image = QImage(resultSize, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(fixed_image)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(fixed_image.rect(), Qt.transparent)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawImage(imagePos(image), image)
        painter.end()
        tool_btn.setIcon(QIcon(QPixmap.fromImage(fixed_image)))
        # self.recalculateResult()
        return fixed_image

    def _getCompositionMode(self):
        box_index = self.operatorComBox.currentIndex()
        return self.operatorComBox.itemData(box_index)

    def chooseSource(self):
        file_name = QFileDialog.getOpenFileName()
        if file_name:
            self._loadImage(file_name[0], self.sourceBtn)

    def chooseDestination(self):
        file_name = QFileDialog.getOpenFileName()
        if file_name:
            self._loadImage(file_name[0], self.destinationBtn)

    def recalculateResult(self):
        com_mode = self._getCompositionMode()
        painter = QPainter(self.resultImage)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(self.resultImage.rect(), Qt.transparent)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawImage(0, 0, self.destinationImage)
        painter.setCompositionMode(com_mode)
        painter.drawImage(0, 0, self.sourceImage)
        painter.fillRect(self.resultImage.rect(), Qt.white)
        painter.end()
        self.resultLabel.setPixmap(QPixmap.fromImage(self.resultImage))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWid = ImageComposer()
    mainWid.show()
    sys.exit(app.exec_())