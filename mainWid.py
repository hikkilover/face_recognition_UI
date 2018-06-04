import sys
import cv2
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5.QtWidgets import qApp, QApplication, QMainWindow, QWidget, QAction, \
    QLabel, QPushButton,\
    QLayout, QHBoxLayout, QVBoxLayout

RowImageHeight = 1280
RowImageWidth = 960
ImageSize = QSize(RowImageHeight, RowImageWidth )


def imagePos(q_image):
    return QPoint(
        (ImageSize.width() - q_image.width())/2,
        (ImageSize.height() - q_image.height()) / 2,
    )


class centralWidget(QWidget):
    def __init__(self):
        super(centralWidget, self).__init__()
        self._createCompents()
        self._createLayout()

    def _createCompents(self):
        # self.closeBtn = QPushButton("close")

        self.imageLabel = QLabel()
        self.imageLabel.setFixedSize(RowImageHeight, RowImageWidth)
        self.imageLabel.setAutoFillBackground(False)

    def _createLayout(self):
        layout = QVBoxLayout()
        # layout.addWidget(self.closeBtn)
        layout.addWidget(self.imageLabel, alignment=Qt.AlignCenter)
        self.setLayout(layout)


class mainWid(QMainWindow):
    def __init__(self, use_camera=False):
        super(mainWid, self).__init__()
        self.showFullScreen()
        self._createStatusBar()
        self._createCentralWid()
        self.cameraFlag = False
        if use_camera:
            self.cap = cv2.VideoCapture(0)
            self.refreshTimer = QTimer()
            self.refreshTimer.timeout.connect(self.refresh)
            if self.cap.isOpened():
                self.cameraFlag = True
                self.showImage = QImage(ImageSize, QImage.Format_ARGB32_Premultiplied)
                self.maskImage = self._loadImage('images/mask.png')
                self.refreshTimer.start(30)
            else:
                self.status.showMessage("摄像头异常", 5000)
                self.cameraFlag = False

    def _createStatusBar(self):
        self.status = self.statusBar()
        self.status.showMessage("这是状态栏", 5000)

    def _createCentralWid(self):
        self.centralWid = centralWidget()
        self.setCentralWidget(self.centralWid)

    # 此函数名不可更改（覆盖了QWidget中的响应函数）
    def keyReleaseEvent(self, event):
        if (event.key() == Qt.Key_Q):
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                if self.cameraFlag:
                    self.cap.release()
                qApp.quit()
            else:
                self.status.showMessage("Ctrl+Q to quit", 1000)

    def refresh(self):
        rct, frame = self.cap.read()
        frame = cv2.cvtColor(cv2.resize(frame, (RowImageHeight, RowImageWidth)), cv2.COLOR_BGR2RGB)
        row_image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        self.addMask(row_image)
        self.centralWid.imageLabel.setPixmap(QPixmap.fromImage(self.showImage))
    
    def _loadImage(self, file_name):
        image = QImage()
        image.load(file_name)
        fixed_image = QImage(ImageSize, QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(fixed_image)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(fixed_image.rect(), Qt.transparent)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawImage(imagePos(image), image)
        painter.end()
        return fixed_image
    
    def addMask(self, row_image):
        com_mode = QPainter.CompositionMode_DestinationAtop
        painter = QPainter(self.showImage)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(row_image.rect(), Qt.transparent)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawImage(0, 0, self.maskImage)
        painter.setCompositionMode(com_mode)
        painter.drawImage(0, 0, row_image)
        painter.fillRect(row_image.rect(), Qt.white)
        painter.end()
        # self.showLabel.setPixmap(QPixmap.fromImage(self.showImage))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWid = mainWid(use_camera=True)
    mainWid.show()
    sys.exit(app.exec_())