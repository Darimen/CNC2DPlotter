from PyQt6.QtGui import QIcon, QTransform, QPixmap
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout


class ToolBar(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.layout = QGridLayout(self)

        self.cursor_button = QPushButton()
        self.select_button = QPushButton()
        self.move_button = QPushButton()

        self.delete_selected_button = QPushButton()
        self.undo_last_draw_button = QPushButton()
        self.draw_line_button = QPushButton()

        self.draw_arc_cw_button = QPushButton()
        self.draw_arc_ccw_button = QPushButton()
        self.send_g_code_button = QPushButton()

        self.action = 'cursor'  # cursor, select, move, delete, undo, line, arc_cw, arc_ccw

        self.initUI()

    def rotateImage(self, angle, path):
        pixmap = QPixmap(path)
        transform = QTransform()
        transform.inverted()
        transform.rotate(angle)
        rotated_pixmap = pixmap.transformed(transform)
        return QIcon(rotated_pixmap)

    def initUI(self):
        # Setting icons for the buttons
        self.cursor_button.setIcon(QIcon("images/cursor.png"))
        self.select_button.setIcon(QIcon("images/selection.png"))
        self.move_button.setIcon(QIcon("images/move.png"))
        self.delete_selected_button.setIcon(QIcon("images/delete.png"))
        self.undo_last_draw_button.setIcon(QIcon("images/undo.png"))
        self.draw_line_button.setIcon(QIcon("images/line.png"))
        self.draw_arc_cw_button.setIcon(self.rotateImage(180, "images/circle_cw.png"))
        self.draw_arc_ccw_button.setIcon(self.rotateImage(0, "images/circle_cw.png"))
        self.send_g_code_button.setIcon(QIcon("images/push.png"))

        # Add buttons to the layout
        self.layout.addWidget(self.cursor_button, 0, 0)
        self.layout.addWidget(self.select_button, 0, 1)
        self.layout.addWidget(self.move_button, 0, 2)
        self.layout.addWidget(self.delete_selected_button, 1, 0)
        self.layout.addWidget(self.undo_last_draw_button, 1, 1)
        self.layout.addWidget(self.draw_line_button, 1, 2)
        self.layout.addWidget(self.draw_arc_cw_button, 2, 0)
        self.layout.addWidget(self.draw_arc_ccw_button, 2, 1)
        self.layout.addWidget(self.send_g_code_button, 2, 2)

        self.cursor_button.setToolTip("Cursor")
        self.select_button.setToolTip("Select")
        self.move_button.setToolTip("Move")
        self.delete_selected_button.setToolTip("Delete Selected")
        self.undo_last_draw_button.setToolTip("Undo Last Draw")
        self.draw_line_button.setToolTip("Draw Line")
        self.draw_arc_cw_button.setToolTip("Draw Arc Clockwise")
        self.draw_arc_ccw_button.setToolTip("Draw Arc Counter Clockwise")
        self.send_g_code_button.setToolTip("Send G-Code to Draw")

        self.attachButtons()

        self.setLayout(self.layout)

    def mouse(self):
        self.action = 'cursor'
        self.parent.setAction(self.action)

    def select(self):
        self.action = 'select'
        self.parent.setAction(self.action)

    def move(self):
        self.action = 'move'
        self.parent.drawing_area.setAction(self.action)

    def delete_selected(self):
        self.parent.drawing_area.removeSelected()

    def undo_last_draw(self):
        self.parent.drawing_area.undoLastDraw()

    def draw_line(self):
        self.action = 'line'
        self.parent.drawing_area.setAction(self.action)

    def draw_arc_cw(self):
        self.action = 'arc_cw'
        self.parent.dialog.show()
        self.parent.drawing_area.setAction(self.action)

    def draw_arc_ccw(self):
        self.action = 'arc_ccw'
        self.parent.dialog.show()
        self.parent.drawing_area.setAction(self.action)

    def send_g_code(self):
        self.parent.g_code_generator.setGCode(self.parent.drawing_area.printDrawings())

    def attachButtons(self):
        self.cursor_button.clicked.connect(self.mouse)
        self.select_button.clicked.connect(self.select)
        self.move_button.clicked.connect(self.move)
        self.delete_selected_button.clicked.connect(self.delete_selected)
        self.undo_last_draw_button.clicked.connect(self.undo_last_draw)
        self.draw_line_button.clicked.connect(self.draw_line)
        self.draw_arc_cw_button.clicked.connect(self.draw_arc_cw)
        self.draw_arc_ccw_button.clicked.connect(self.draw_arc_ccw)
        self.send_g_code_button.clicked.connect(self.send_g_code)

