from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QApplication


class ArcInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent

        self.angle_input = QLineEdit()  # rotation
        self.radius_input = QLineEdit()  # radius
        self.span_angle_input = QLineEdit()  # span angle

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter Arc Angle (degrees):"))
        layout.addWidget(self.angle_input)
        layout.addWidget(QLabel("Enter Arc Radius:"))
        layout.addWidget(self.radius_input)
        layout.addWidget(QLabel("Enter Arc Span Angle:"))
        layout.addWidget(self.span_angle_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def accept(self):
        self.parent.setAngle(int(self.angle_input.text()))
        self.parent.setRadius(int(self.radius_input.text()))
        self.parent.setSpanAngle(int(self.span_angle_input.text()))
        self.hide()

    def reject(self):
        self.hide()
