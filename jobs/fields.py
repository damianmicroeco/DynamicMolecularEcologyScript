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
)
from PySide6.QtCore import Signal


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
    ):
        super().__init__(
            label,
            template,
            visible,
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
    ):
        super().__init__(
            label,
            template,
            visible,
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
    ):
        super().__init__(
            label,
            template,
            visible,
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
    ):
        super().__init__(
            label,
            template,
            visible,
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
    ):
        super().__init__(
            label,
            template,
            visible,
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
    ):
        super().__init__(
            label,
            template,
            visible,
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
):
    return TextField(
        label=label,
        template=template,
        default=default,
    )


def integer(
    label,
    template=None,
    minimum=0,
    maximum=100,
    default=0,
):
    return IntField(
        label=label,
        template=template,
        minimum=minimum,
        maximum=maximum,
        default=default,
    )


def floating(
    label,
    template=None,
    minimum=0.0,
    maximum=100.0,
    default=0.0,
    decimals=2,
    step=0.1,
):
    return FloatField(
        label=label,
        template=template,
        minimum=minimum,
        maximum=maximum,
        default=default,
        decimals=decimals,
        step=step,
    )


def combo(
    label,
    choices,
    template=None,
    default=None,
):
    return ComboField(
        label=label,
        choices=choices,
        template=template,
        default=default,
    )


def checkbox(
    label,
    template=None,
    default=False,
):
    return CheckField(
        label=label,
        template=template,
        default=default,
    )


def path(
    label,
    template=None,
    mode="file",
    default="",
):
    return PathField(
        label=label,
        template=template,
        mode=mode,
        default=default,
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
    "visible_when",
]