import sys
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QWidget, QLabel, QGridLayout, QMainWindow, QVBoxLayout,
    QVBoxLayout, QLabel, QHBoxLayout, QApplication
)

from drawingArea import DrawingArea
from toolBar import ToolBar
from arcDialog import ArcInputDialog
from gCodeGen import GCodeGenerator


class CNCMachineGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget = QWidget()
        self.drawing_area = DrawingArea()
        self.tool_layout = ToolBar(parent=self)
        self.ruler_y_layout = QVBoxLayout()
        self.ruler_x_layout = QHBoxLayout()
        self.canvas_layout = QVBoxLayout()
        self.main_layout = QGridLayout()
        self.dialog = ArcInputDialog(parent=self)

        self.setGeometry(100, 100, 1187, 900)

        self.move(250, 25)
        self.x_pos = 0
        self.y_pos = 0

        self.label_ruler_x = QLabel("x:" + str(self.x_pos), self)
        self.label_ruler_y = QLabel("y:" + str(self.y_pos), self)
        self.label_drawing = None
        self.label_drawing_radius = None
        self.radius = 0

        self.drawing = None
        self.selected_button = None
        self.initUI()
        self.tool_layout = None

        self.g_code_generator = GCodeGenerator()

    def initUI(self):
        # Main widget and layout
        self.main_layout.addWidget(self.tool_layout, 0, 0, 1, 1)
        self.main_layout.addLayout(self.ruler_y_layout, 1, 0, 7, 1)
        self.main_layout.addLayout(self.ruler_x_layout, 7, 1, 1, 7)
        self.main_layout.addLayout(self.canvas_layout, 0, 1, 7, 7)

        self.ruler_y_layout.addWidget(self.label_ruler_y)
        self.ruler_x_layout.addWidget(self.label_ruler_x)
        self.canvas_layout.addWidget(self.drawing_area)

        # setting layout
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        # setting window title
        self.setWindowTitle('CNC Machine GUI')

        # showing window
        self.show()

    def setAction(self, action):
        self.drawing_area.setAction(action)

    def setAngle(self, angle):
        self.drawing_area.setAngle(angle)

    def setRadius(self, radius):
        self.drawing_area.setRadius(radius)

    def setSpanAngle(self, spanAngle):
        self.drawing_area.setSpanAngle(spanAngle)


def main():
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    main_window = CNCMachineGUI()
    main_window.show()

    # Run the application's main loop
    sys.exit(app.exec())


if __name__ == "__main__":
    # Create the application and main window
    main()
