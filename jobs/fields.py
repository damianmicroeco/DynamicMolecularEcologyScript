#!/usr/bin/env python3

from __future__ import annotations

from abc import ABC, abstractmethod

from PySide6.QtWidgets import (
    QWidget,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QVBoxLayout,
<<<<<<< HEAD
=======
    QGridLayout,
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)

from PySide6.QtCore import Signal, Qt

import csv


# ----------------------------------------------------------------------
# Path Selector
# ----------------------------------------------------------------------

class PathSelector(QWidget):
    pathChanged = Signal(str)

    def __init__(self, mode="file", parent=None):
        super().__init__(parent)

        self.mode = mode

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.line_edit = QLineEdit()

        self.button = QPushButton("Browse")
        self.button.clicked.connect(self.browse)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

    def browse(self):
        if self.mode == "directory":
            path = QFileDialog.getExistingDirectory(
                self,
                "Select Directory",
            )
        else:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Select File",
            )

        if path:
            self.line_edit.setText(path)
            self.pathChanged.emit(path)

    def text(self):
        return self.line_edit.text()

    def setText(self, value):

        value = str(value)

        self.line_edit.setText(value)

        self.pathChanged.emit(value)

<<<<<<< HEAD
# ----------------------------------------------------------------------
# Spreadsheet Editor
# ----------------------------------------------------------------------

class SpreadsheetEditor(QWidget):
    """
    Editable spreadsheet-like widget.

    Supports:

      • direct cell editing
      • copy/paste from spreadsheets
      • CSV import
      • CSV export
      • adding/removing rows
      • adding/removing columns

    The underlying data is represented as:
=======
class SpreadsheetEditor(QWidget):
    """
    Generic editable spreadsheet-like widget.

    The spreadsheet itself knows nothing about the meaning of
    individual columns. The parent widget supplies the column names.

    Data is represented as:
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)

        [
            ["value", "value"],
            ["value", "value"],
        ]

<<<<<<< HEAD
    All values are stored as strings so the result is JSON-compatible.
=======
    All values are stored as strings.
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
    """

    dataChanged = Signal()

    def __init__(
        self,
<<<<<<< HEAD
        columns=None,
=======
        columns,
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
        rows=3,
        parent=None,
    ):
        super().__init__(parent)

<<<<<<< HEAD
        self.columns = list(columns or ["Column 1", "Column 2"])
=======
        if not columns:
            raise ValueError(
                "SpreadsheetEditor requires at least one column."
            )

        self.columns = list(columns)
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)

        self._loading = False

        layout = QVBoxLayout(self)

        # ---------------------------------------------------------
        # Table
        # ---------------------------------------------------------

        self.table = QTableWidget(
            rows,
            len(self.columns),
            self,
        )

<<<<<<< HEAD
=======
        self.table.setMinimumHeight(260)

>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
        self.table.setHorizontalHeaderLabels(
            self.columns
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setSelectionMode(
            QTableWidget.ContiguousSelection
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectItems
        )

        self.table.setAlternatingRowColors(True)

        self.table.cellChanged.connect(
            self._on_cell_changed
        )

        layout.addWidget(self.table)

        # ---------------------------------------------------------
        # Buttons
        # ---------------------------------------------------------

<<<<<<< HEAD
        button_layout = QHBoxLayout()

        self.add_row_button = QPushButton(
            "Add Row"
        )

        self.remove_row_button = QPushButton(
            "Remove Row"
        )

        self.add_column_button = QPushButton(
            "Add Column"
        )

        self.remove_column_button = QPushButton(
            "Remove Column"
        )

        self.import_button = QPushButton(
            "Import CSV"
        )

        self.export_button = QPushButton(
            "Export CSV"
        )

        button_layout.addWidget(
            self.add_row_button
        )

        button_layout.addWidget(
            self.remove_row_button
        )

        button_layout.addWidget(
            self.add_column_button
        )

        button_layout.addWidget(
            self.remove_column_button
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.import_button
        )

        button_layout.addWidget(
            self.export_button
        )

=======
        button_layout = QGridLayout()

        self.add_row_button = QPushButton("Add Row")
        self.remove_row_button = QPushButton("Remove Row")
        self.add_column_button = QPushButton("Add Column")
        self.remove_column_button = QPushButton("Remove Column")
        self.import_button = QPushButton("Import CSV")
        self.export_button = QPushButton("Export CSV")

        button_layout.addWidget(
            self.add_row_button, 0, 0
        )

        button_layout.addWidget(
            self.remove_row_button, 0, 1
        )

        button_layout.addWidget(
            self.add_column_button, 0, 2
        )

        button_layout.addWidget(
            self.remove_column_button, 1, 0
        )

        button_layout.addWidget(
            self.import_button, 1, 1
        )

        button_layout.addWidget(
            self.export_button, 1, 2
        )

        button_layout.setColumnStretch(0, 1)
        button_layout.setColumnStretch(1, 1)
        button_layout.setColumnStretch(2, 1)

>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
        layout.addLayout(button_layout)

        # ---------------------------------------------------------
        # Connections
        # ---------------------------------------------------------

        self.add_row_button.clicked.connect(
            self.add_row
        )

        self.remove_row_button.clicked.connect(
            self.remove_row
        )

        self.add_column_button.clicked.connect(
            self.add_column
        )

        self.remove_column_button.clicked.connect(
            self.remove_column
        )

        self.import_button.clicked.connect(
            self.import_csv
        )

        self.export_button.clicked.connect(
            self.export_csv
        )

    # ---------------------------------------------------------
    # Cell changes
    # ---------------------------------------------------------

    def _on_cell_changed(self, row, column):

        if self._loading:
            return

        self.dataChanged.emit()

    # ---------------------------------------------------------
    # Rows
    # ---------------------------------------------------------

    def add_row(self):

        row = self.table.rowCount()

        self.table.insertRow(row)

        self.dataChanged.emit()

    def remove_row(self):

        row = self.table.currentRow()

        if row < 0:
            return

        self.table.removeRow(row)

        self.dataChanged.emit()

    # ---------------------------------------------------------
    # Columns
    # ---------------------------------------------------------

    def add_column(self):

        column = self.table.columnCount()

        self.table.insertColumn(column)

<<<<<<< HEAD
        self.table.setHorizontalHeaderItem(
            column,
            QTableWidgetItem(
                f"Column {column + 1}"
            ),
=======
        name = f"Column {column + 1}"

        self.table.setHorizontalHeaderItem(
            column,
            QTableWidgetItem(name),
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
        )

        self.dataChanged.emit()

    def remove_column(self):

        column = self.table.currentColumn()

        if column < 0:
            return

        if self.table.columnCount() <= 1:
            return

        self.table.removeColumn(column)

        self.dataChanged.emit()

    # ---------------------------------------------------------
    # Data
    # ---------------------------------------------------------

    def value(self):
<<<<<<< HEAD
        """
        Return the table as a list of rows.
        """
=======
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)

        data = []

        for row in range(
            self.table.rowCount()
        ):

            values = []

            for column in range(
                self.table.columnCount()
            ):

                item = self.table.item(
                    row,
                    column,
                )

<<<<<<< HEAD
                if item is None:
                    values.append("")
                else:
                    values.append(
                        item.text()
                    )
=======
                values.append(
                    "" if item is None
                    else item.text()
                )
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)

            data.append(values)

        return data

    # ---------------------------------------------------------

    def set_value(self, data):
<<<<<<< HEAD
        """
        Restore the table from a list of rows.

        Expected format:

            [
                ["a", "b"],
                ["c", "d"],
            ]
        """
=======
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)

        if not isinstance(data, list):
            return

        self._loading = True

        try:

            if not data:
                self.table.setRowCount(0)
                return

<<<<<<< HEAD
            # Determine maximum number of columns.
=======
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
            column_count = max(
                len(row)
                for row in data
                if isinstance(row, list)
            )

            if column_count <= 0:
                return

            self.table.setColumnCount(
                column_count
            )

<<<<<<< HEAD
            # Preserve existing column names where possible.
            for column in range(column_count):

                if column < len(self.columns):

                    name = self.columns[column]

                else:

                    name = (
                        f"Column {column + 1}"
                    )
=======
            for column in range(column_count):

                if column < len(self.columns):
                    name = self.columns[column]
                else:
                    name = f"Column {column + 1}"
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)

                self.table.setHorizontalHeaderItem(
                    column,
                    QTableWidgetItem(name),
                )

            self.table.setRowCount(
                len(data)
            )

            for row_index, row in enumerate(data):

                if not isinstance(row, list):
                    continue

                for column_index, value in enumerate(row):

                    if column_index >= column_count:
                        break

                    item = QTableWidgetItem(
                        "" if value is None
                        else str(value)
                    )

                    self.table.setItem(
                        row_index,
                        column_index,
                        item,
                    )

        finally:

            self._loading = False

    # ---------------------------------------------------------
    # CSV Import
    # ---------------------------------------------------------

    def import_csv(self):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import CSV",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )

        if not path:
            return

        try:

            with open(
                path,
                "r",
                newline="",
                encoding="utf-8-sig",
            ) as handle:

                reader = csv.reader(handle)
<<<<<<< HEAD

=======
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
                rows = list(reader)

            if not rows:
                return

<<<<<<< HEAD
            # -------------------------------------------------
            # Treat the first row as headers only if it
            # resembles the configured headers.
            #
            # Otherwise import every row as data.
            # -------------------------------------------------

=======
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
            first_row = rows[0]

            if (
                self.columns
                and first_row == self.columns
            ):
                data = rows[1:]
<<<<<<< HEAD

=======
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
            else:
                data = rows

            self.set_value(data)

            self.dataChanged.emit()

        except Exception as exc:

            QMessageBox.critical(
                self,
                "CSV Import Error",
                f"Could not import CSV file:\n\n{exc}",
            )

    # ---------------------------------------------------------
    # CSV Export
    # ---------------------------------------------------------

    def export_csv(self):

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export CSV",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )

        if not path:
            return

        try:

            with open(
                path,
                "w",
                newline="",
                encoding="utf-8",
            ) as handle:

                writer = csv.writer(handle)

<<<<<<< HEAD
                # Header row
=======
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
                headers = []

                for column in range(
                    self.table.columnCount()
                ):

                    item = (
                        self.table.horizontalHeaderItem(
                            column
                        )
                    )

                    headers.append(
                        item.text()
                        if item is not None
                        else f"Column {column + 1}"
                    )

                writer.writerow(headers)

<<<<<<< HEAD
                # Data
                for row in self.value():

=======
                for row in self.value():
>>>>>>> e06114a (Restructuring: movement and restructure on Fir cluster because of internet connection issues on Rorqual cluster)
                    writer.writerow(row)

        except Exception as exc:

            QMessageBox.critical(
                self,
                "CSV Export Error",
                f"Could not export CSV file:\n\n{exc}",
            )

# ----------------------------------------------------------------------
# Base Field
# ----------------------------------------------------------------------

class Field(ABC):
    """
    Abstract base class for all editable fields.

    A Field is responsible for:

      • creating its Qt widget
      • reading its value
      • restoring its value
      • connecting change notifications
      • cloning itself for widget instances
    """

    def __init__(
        self,
        label,
        template=None,
        visible=True,
        help_text=None,
    ):
        self.label = label

        self.template = (
            template
            if template is not None
            else (
                label.upper()
                     .replace(" ", "_")
                     .replace("-", "_")
                     .replace("(", "")
                     .replace(")", "")
            )
        )

        self.visible = visible
        self.help_text = help_text

        self.widget = None
        self.label_widget = None

        self.show_when = None

    @abstractmethod
    def create_widget(self):
        pass

    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def set_value(self, value):
        pass

    @abstractmethod
    def connect(self, callback):
        pass

    def clone(self):
        """
        Create a clean copy of this field definition.

        Widgets and labels are intentionally not copied because
        every WidgetItem instance needs its own Qt objects.
        """

        import copy

        cloned = copy.copy(self)

        cloned.widget = None
        cloned.label_widget = None

        return cloned

    def set_visibility_rule(
        self,
        controller,
        value,
    ):
        self.show_when = (
            controller,
            value,
        )

        return self

    def set_visible(
        self,
        visible,
    ):
        if self.label_widget is not None:
            self.label_widget.setVisible(visible)

        if self.widget is not None:
            self.widget.setVisible(visible)

# ----------------------------------------------------------------------
# Text Field
# ----------------------------------------------------------------------

class TextField(Field):

    def __init__(
        self,
        label,
        template=None,
        default="",
        visible=True,
        help_text=None,
    ):
        super().__init__(
            label,
            template,
            visible,
            help_text,
        )

        self.default = default

    def create_widget(self):
        self.widget = QLineEdit()

        self.widget.setText(self.default)

        return self.widget

    def value(self):
        return self.widget.text()

    def set_value(self, value):
        self.widget.setText("" if value is None else str(value))

    def connect(self, callback):
        self.widget.textChanged.connect(callback)


# ----------------------------------------------------------------------
# Integer Field
# ----------------------------------------------------------------------

class IntField(Field):

    def __init__(
        self,
        label,
        template=None,
        minimum=0,
        maximum=100,
        default=0,
        visible=True,
        help_text=None,
    ):
        super().__init__(
            label,
            template,
            visible,
            help_text
        )

        self.minimum = minimum
        self.maximum = maximum
        self.default = default

    def create_widget(self):
        self.widget = QSpinBox()

        self.widget.setRange(
            self.minimum,
            self.maximum,
        )

        self.widget.setValue(
            self.default,
        )

        return self.widget

    def value(self):
        return self.widget.value()

    def set_value(self, value):
        self.widget.setValue(int(value))

    def connect(self, callback):
        self.widget.valueChanged.connect(callback)


# ----------------------------------------------------------------------
# Float Field
# ----------------------------------------------------------------------

class FloatField(Field):

    def __init__(
        self,
        label,
        template=None,
        minimum=0.0,
        maximum=100.0,
        default=0.0,
        decimals=2,
        step=0.1,
        visible=True,
        help_text=None,
    ):
        super().__init__(
            label,
            template,
            visible,
            help_text
        )

        self.minimum = minimum
        self.maximum = maximum
        self.default = default
        self.decimals = decimals
        self.step = step

    def create_widget(self):
        self.widget = QDoubleSpinBox()

        self.widget.setRange(
            self.minimum,
            self.maximum,
        )

        self.widget.setDecimals(
            self.decimals,
        )

        self.widget.setSingleStep(
            self.step,
        )

        self.widget.setValue(
            self.default,
        )

        return self.widget

    def value(self):
        return self.widget.value()

    def set_value(self, value):
        self.widget.setValue(float(value))

    def connect(self, callback):
        self.widget.valueChanged.connect(callback)

# ----------------------------------------------------------------------
# Combo Field
# ----------------------------------------------------------------------

class ComboField(Field):

    def __init__(
        self,
        label,
        choices,
        template=None,
        default=None,
        visible=True,
        help_text=None,
    ):
        super().__init__(
            label,
            template,
            visible,
            help_text,
        )

        self.choices = list(choices)
        self.default = default

    def create_widget(self):
        self.widget = QComboBox()

        self.widget.addItems(self.choices)

        if self.default is not None:
            index = self.widget.findText(str(self.default))
            if index >= 0:
                self.widget.setCurrentIndex(index)

        return self.widget

    def value(self):
        return self.widget.currentText()

    def set_value(self, value):
        index = self.widget.findText(str(value))
        if index >= 0:
            self.widget.setCurrentIndex(index)

    def connect(self, callback):
        self.widget.currentTextChanged.connect(callback)


# ----------------------------------------------------------------------
# Check Box Field
# ----------------------------------------------------------------------

class CheckField(Field):

    def __init__(
        self,
        label,
        template=None,
        default=False,
        visible=True,
        help_text=None,
    ):
        super().__init__(
            label,
            template,
            visible,
            help_text,
        )

        self.default = default

    def create_widget(self):
        self.widget = QCheckBox()

        self.widget.setChecked(self.default)

        return self.widget

    def value(self):
        return self.widget.isChecked()

    def set_value(self, value):
        self.widget.setChecked(bool(value))

    def connect(self, callback):
        self.widget.toggled.connect(callback)


# ----------------------------------------------------------------------
# Path Field
# ----------------------------------------------------------------------

class PathField(Field):

    def __init__(
        self,
        label,
        template=None,
        mode="file",
        default="",
        visible=True,
        help_text=None,
    ):
        super().__init__(
            label,
            template,
            visible,
            help_text,
        )

        self.mode = mode
        self.default = default

    def create_widget(self):
        self.widget = PathSelector(
            mode=self.mode,
        )

        if self.default:
            self.widget.setText(self.default)

        return self.widget

    def value(self):
        return self.widget.text()

    def set_value(self, value):
        self.widget.setText("" if value is None else str(value))

    def connect(self, callback):
        self.widget.pathChanged.connect(callback)

# ----------------------------------------------------------------------
# Spreadsheet Field
# ----------------------------------------------------------------------

class SpreadsheetField(Field):
    """
    Field containing an editable spreadsheet.

    Parameters
    ----------
    columns : list[str]
        Column headers.

    rows : int
        Initial number of empty rows.

    default : list[list]
        Optional initial table contents.

    date_columns : list[int] | None
        Optional zero-based column indexes containing dates.

        This is currently metadata used by validation. Values remain
        strings so that CSV imports and serialization remain simple.
    """

    def __init__(
        self,
        label,
        columns=None,
        template=None,
        rows=3,
        default=None,
        date_columns=None,
        visible=True,
        help_text=None,
    ):

        super().__init__(
            label,
            template,
            visible,
            help_text,
        )

        self.columns = list(
            columns or ["Column 1", "Column 2"]
        )

        self.rows = rows

        self.default = (
            default
            if default is not None
            else []
        )

        self.date_columns = list(
            date_columns or []
        )

    # ---------------------------------------------------------

    def create_widget(self):

        self.widget = SpreadsheetEditor(
            columns=self.columns,
            rows=self.rows,
        )

        if self.default:
            self.widget.set_value(
                self.default
            )

        return self.widget

    # ---------------------------------------------------------

    def value(self):

        return self.widget.value()

    # ---------------------------------------------------------

    def set_value(self, value):

        self.widget.set_value(value)

    # ---------------------------------------------------------

    def connect(self, callback):

        self.widget.dataChanged.connect(
            callback
        )

    # ---------------------------------------------------------

    def validate(self):

        if not self.date_columns:
            return True, ""

        for row_index, row in enumerate(
            self.value(),
            start=1,
        ):

            # Completely empty rows are ignored.
            if not any(
                str(value).strip()
                for value in row
            ):
                continue

            for column_index in self.date_columns:

                if column_index >= len(row):
                    continue

                value = str(
                    row[column_index]
                ).strip()

                if not value:
                    continue

                if not self._is_valid_date(
                    value
                ):
                    return (
                        False,
                        (
                            f"Invalid date "
                            f"'{value}' in row "
                            f"{row_index}."
                        ),
                    )

        return True, ""

    # ---------------------------------------------------------

    @staticmethod
    def _is_valid_date(value):

        from datetime import datetime

        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%m/%d/%Y",
            "%m-%d-%Y",
            "%d/%m/%Y",
            "%d-%m-%Y",
        ]

        for date_format in formats:

            try:

                datetime.strptime(
                    value,
                    date_format,
                )

                return True

            except ValueError:
                pass

        return False

# ----------------------------------------------------------------------
# Serialization Helpers
# ----------------------------------------------------------------------

def serialize_fields(fields):
    """
    Convert a list of Field objects into a serializable dictionary.
    """
    return {
        field.label: field.value()
        for field in fields
    }


def restore_fields(fields, values):
    """
    Restore a previously serialized dictionary of values.
    """
    if not isinstance(values, dict):
        return

    lookup = {
        field.label: field
        for field in fields
    }

    for label, value in values.items():
        field = lookup.get(label)

        if field is None:
            continue

        field.set_value(value)


def template_context(fields):
    """
    Generate a template replacement dictionary from a list of fields.
    """
    return {
        field.template: field.value()
        for field in fields
    }

# ----------------------------------------------------------------------
# Convenience Factory Functions
# ----------------------------------------------------------------------

def text(
    label,
    template=None,
    default="",
    help_text=None,
):
    return TextField(
        label=label,
        template=template,
        default=default,
        help_text=help_text,
    )


def integer(
    label,
    template=None,
    minimum=0,
    maximum=100,
    default=0,
    help_text=None,
):
    return IntField(
        label=label,
        template=template,
        minimum=minimum,
        maximum=maximum,
        default=default,
        help_text=help_text,
    )


def floating(
    label,
    template=None,
    minimum=0.0,
    maximum=100.0,
    default=0.0,
    decimals=2,
    step=0.1,
    help_text=None,
):
    return FloatField(
        label=label,
        template=template,
        minimum=minimum,
        maximum=maximum,
        default=default,
        decimals=decimals,
        step=step,
        help_text=help_text,
    )


def combo(
    label,
    choices,
    template=None,
    default=None,
    help_text=None,
):
    return ComboField(
        label=label,
        choices=choices,
        template=template,
        default=default,
        help_text=help_text,
    )


def checkbox(
    label,
    template=None,
    default=False,
    help_text=None,
):
    return CheckField(
        label=label,
        template=template,
        default=default,
        help_text=help_text,
    )


def path(
    label,
    template=None,
    mode="file",
    default="",
    help_text=None,
):
    return PathField(
        label=label,
        template=template,
        mode=mode,
        default=default,
        help_text=help_text,
    )

def spreadsheet(
    label,
    columns=None,
    template=None,
    rows=3,
    default=None,
    date_columns=None,
    help_text=None,
):
    return SpreadsheetField(
        label=label,
        columns=columns,
        template=template,
        rows=rows,
        default=default,
        date_columns=date_columns,
        help_text=help_text,
    )

def visible_when(
    field,
    controller,
    value,
):
    field.set_visibility_rule(
        controller,
        value,
    )

    return field

__all__ = [
    "Field",
    "TextField",
    "IntField",
    "FloatField",
    "ComboField",
    "CheckField",
    "PathField",
    "PathSelector",
    "serialize_fields",
    "restore_fields",
    "template_context",
    "text",
    "integer",
    "floating",
    "combo",
    "checkbox",
    "path",
    "spreadsheet",
    "visible_when",
]