#!/usr/bin/env python3

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow


def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    return app.exec()


if __name__ == "__main__":

    sys.exit(
        main()
    )