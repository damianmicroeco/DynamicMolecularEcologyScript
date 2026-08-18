#!/usr/bin/env python3

from __future__ import annotations

import sys
import json

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QScrollArea,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QTreeView,
)

from PySide6.QtGui import (
    QStandardItem,
    QStandardItemModel,
)

from widget_base import WidgetItem

# Importing widgets registers all widget classes
import widgets



class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Dynamic Template Script Builder"
        )

        self.resize(
            1000,
            600,
        )

        self.active_widgets = []

        self.widget_counts = {}

        # -----------------------------------------------------
        # Main layout
        # -----------------------------------------------------

        main_widget = QWidget()

        self.setCentralWidget(
            main_widget
        )

        main_layout = QHBoxLayout(
            main_widget
        )


        # -----------------------------------------------------
        # Left panel
        # -----------------------------------------------------

        left_container = QWidget()

        left_layout = QVBoxLayout(
            left_container
        )


        # -----------------------------------------------------
        # Save / Load toolbar
        # -----------------------------------------------------

        toolbar = QHBoxLayout()

        self.save_btn = QPushButton(
            "💾 Save Template & Script"
        )

        self.load_btn = QPushButton(
            "📂 Load Template JSON"
        )

        self.save_btn.clicked.connect(
            self.save_template
        )

        self.load_btn.clicked.connect(
            self.load_template
        )

        toolbar.addWidget(
            self.save_btn
        )

        toolbar.addWidget(
            self.load_btn
        )

        left_layout.addLayout(
            toolbar
        )


        # -----------------------------------------------------
        # Widget selector
        # -----------------------------------------------------

        self.selector = QComboBox()

        self.selector_model = (
            QStandardItemModel()
        )

        self.selector_model.appendRow(
            QStandardItem("-- Select --")
        )

        self.populate_widget_selector()

        self.selector.setModel(
            self.selector_model
        )


        tree = QTreeView()

        tree.setHeaderHidden(
            True
        )

        tree.expandAll()

        self.selector.setView(
            tree
        )

        self.selector.activated.connect(
            self.add_widget_from_selection
        )

        left_layout.addWidget(
            self.selector
        )


        # -----------------------------------------------------
        # Dynamic widget area
        # -----------------------------------------------------

        self.scroll_area = QScrollArea()

        self.scroll_area.setWidgetResizable(
            True
        )

        self.scroll_widget = QWidget()

        self.scroll_layout = QVBoxLayout(
            self.scroll_widget
        )

        self.scroll_layout.setAlignment(
            Qt.AlignTop
        )

        self.scroll_area.setWidget(
            self.scroll_widget
        )

        left_layout.addWidget(
            self.scroll_area
        )


        # -----------------------------------------------------
        # Preview panel
        # -----------------------------------------------------

        right_container = QWidget()

        right_layout = QVBoxLayout(
            right_container
        )

        right_layout.addWidget(
            QLabel(
                "<b>Generated Script Preview:</b>"
            )
        )

        self.script_preview = QTextEdit()

        self.script_preview.setReadOnly(
            True
        )

        right_layout.addWidget(
            self.script_preview
        )


        main_layout.addWidget(
            left_container,
            stretch=1,
        )

        main_layout.addWidget(
            right_container,
            stretch=1,
        )


        self.update_template_script()



    # =========================================================
    # Widget discovery
    # =========================================================

    def populate_widget_selector(self):

        """
        Build selector entries from registered widgets.

        No widget classes are referenced here.
        """

        for widget_type, widget_class in (
            WidgetItem.registered_types()
            .items()
        ):

            item = QStandardItem(
                widget_class.display_name()
            )

            item.setData(
                widget_type
            )

            self.selector_model.appendRow(
                item
            )



    # =========================================================
    # Widget creation
    # =========================================================
    def extract_widget_number(self, key):
        """
        Extract the numeric suffix from widget keys.

        Example:
            aligner_3 -> 3

        Returns:
            0 if no numeric suffix exists.
        """

        try:
            return int(
                key.rsplit("_", 1)[1]
            )

        except (ValueError, IndexError):
            return 0

    def add_widget_from_selection(
        self,
        index,
    ):

        item = (
            self.selector_model
            .item(index)
        )

        if item is None:
            return


        widget_type = item.data()


        if widget_type is None:
            return


        widget_class = (
            WidgetItem.from_type(
                widget_type
            )
        )


        if widget_class is None:
            return


        count = (
            self.widget_counts
            .get(widget_type, 0)
            + 1
        )


        self.widget_counts[
            widget_type
        ] = count


        key = (
            f"{widget_type}_{count}"
        )


        widget = (
            self.create_and_append_widget(
                widget_class,
                key,
            )
        )


        self.selector.setCurrentIndex(
            0
        )



    def create_and_append_widget(
        self,
        widget_class,
        key,
        values=None,
    ):

        widget = widget_class.create(
            key=key,
            change_callback=self.update_template_script,
            values=values,
        )


        widget.remove_btn.clicked.connect(
            lambda: self.remove_custom_widget(
                widget
            )
        )


        self.scroll_layout.addWidget(
            widget
        )

        self.active_widgets.append(
            widget
        )

        self.update_template_script()

        return widget

    # =========================================================
    # Widget removal
    # =========================================================

    def remove_custom_widget(
        self,
        widget,
    ):

        if widget in self.active_widgets:

            self.active_widgets.remove(
                widget
            )

        self.scroll_layout.removeWidget(
            widget
        )

        widget.deleteLater()

        self.update_template_script()



    # =========================================================
    # Template generation
    # =========================================================

    def build_script_text(self):

        parts = []

        for widget in self.active_widgets:

            if not widget.is_valid():
                continue

            fragment = (
                widget.build_script_fragment(
                    Path(__file__).parent /
                    "module_templates"
                )
            )

            if fragment.strip():

                parts.append(
                    fragment
                )


        return "\n\n".join(
            parts
        )



    def update_template_script(self):

        try:

            self.script_preview.setPlainText(
                self.build_script_text()
            )


        except Exception as error:

            self.script_preview.setPlainText(
                "TEMPLATE ERROR:\n\n"
                + str(error)
            )



    # =========================================================
    # Save / Load
    # =========================================================

    def save_template(self):

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Template",
            "",
            (
                "Bash Scripts (*.bash);;"
                "Shell Scripts (*.sh);;"
                "Python Script (*.py);;"
                "All Files (*)"
            ),
        )


        if not file_path:

            return


        script_path = Path(
            file_path
        )

        json_path = (
            script_path
            .with_suffix(".json")
        )


        state = {

            "widget_counts":
                self.widget_counts,


            "widgets":

                [

                    {
                        "type":
                            widget.widget_type(),

                        "key":
                            widget.key,

                        "label":
                            widget.TITLE,

                        "value":
                            widget.get_raw_value(),

                    }

                    for widget
                    in self.active_widgets

                ],
        }


        try:

            script_path.write_text(
                self.build_script_text(),
                encoding="utf-8",
            )


            json_path.write_text(
                json.dumps(
                    state,
                    indent=4,
                ),
                encoding="utf-8",
            )


            QMessageBox.information(
                self,
                "Saved",
                "Template saved successfully.",
            )


        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                str(error),
            )



    def load_template(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Template",
            "",
            "JSON (*.json)",
        )


        if not file_path:

            return


        try:

            data = json.loads(
                Path(file_path)
                .read_text(
                    encoding="utf-8"
                )
            )


            # -------------------------------------------------
            # Clear existing widgets
            # -------------------------------------------------

            for widget in list(
                self.active_widgets
            ):

                self.remove_custom_widget(
                    widget
                )


            self.widget_counts = {}

            # -------------------------------------------------
            # Restore widgets dynamically
            # -------------------------------------------------

            for item in data.get(
                "widgets",
                [],
            ):


                widget_class = (
                    WidgetItem.from_type(
                        item["type"]
                    )
                )


                if widget_class is None:

                    continue


                widget = self.create_and_append_widget(
                        widget_class,
                        item["key"],
                        item.get(
                            "value"
                        ),
                    )
                
                widget_type = widget.widget_type()

                current_count = self.widget_counts.get(
                    widget_type,
                    0,
                )

                self.widget_counts[widget_type] = (
                    max(
                        current_count,
                        self.extract_widget_number(widget.key),
                    )
                )


            QMessageBox.information(
                self,
                "Loaded",
                "Template restored.",
            )


        except Exception as error:

            QMessageBox.critical(
                self,
                "Load Error",
                str(error),
            )



# =============================================================
# Application entry point
# =============================================================
stylesheet_path = (
    Path(__file__).resolve().parent
    / "styles"
    / "app.qss"
)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    app.setStyleSheet(
        stylesheet_path.read_text(
            encoding="utf-8"
        )
    )

    window = MainWindow()

    window.show()


    sys.exit(
        app.exec()
    )