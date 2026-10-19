#!/usr/bin/env python3

import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
)


app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("PySide6 Rendering Test")
window.resize(600, 400)

central = QWidget()
layout = QVBoxLayout(central)

label = QLabel("PySide6 X11 rendering test")
layout.addWidget(label)

for i in range(10):
    button = QPushButton(f"Button {i + 1}")
    layout.addWidget(button)

window.setCentralWidget(central)
window.show()

sys.exit(app.exec())