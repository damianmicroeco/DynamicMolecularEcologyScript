#!/usr/bin/env python3

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from main_window import MainWindow

from pathlib import Path


def main():
    app = QApplication(sys.argv)

    stylesheet_path = (
        Path(__file__).resolve().parent
        / "styles"
        / "app.qss"
    )

    print(
        f"Loading stylesheet: {stylesheet_path}"
    )

    if not stylesheet_path.is_file():

        raise FileNotFoundError(
            f"Stylesheet not found:\n{stylesheet_path}"
        )

    stylesheet = stylesheet_path.read_text(
        encoding="utf-8"
    )

    print(
        f"Loaded stylesheet: "
        f"{len(stylesheet)} characters"
    )

    app.setStyleSheet(
        stylesheet
    )

    window = MainWindow()

    window.show()

    return app.exec()


if __name__ == "__main__":

    sys.exit(
        main()
    )