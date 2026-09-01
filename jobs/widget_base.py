#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)

from fields import (
    serialize_fields,
    restore_fields,
    template_context,
)


class WidgetItem(QFrame):
    """
    Generic base class for every dynamically created widget.

    Subclasses typically only define:

        TYPE
        TITLE
        TEMPLATE
        FIELDS

    and optionally override:

        get_template_context()
        build_script_fragment()

    Everything else is handled automatically.
    """

    TYPE = "base"
    TITLE = "Widget"
    TEMPLATE = None
    FIELDS = []

    registry = {}

    # ---------------------------------------------------------
    # Automatic registration
    # ---------------------------------------------------------

    def __init_subclass__(cls, **kwargs):

        super().__init_subclass__(**kwargs)

        widget_type = getattr(cls, "TYPE", None)

        if widget_type and widget_type != "base":
            WidgetItem.registry[widget_type] = cls

    # ---------------------------------------------------------

    def __init__(
        self,
        key,
        label=None,
        change_callback=None,
        parent=None,
    ):
        super().__init__(parent)

        self.key = key
        self.change_callback = change_callback or (lambda *args: None)

        self.fields = []

        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(1)

        self.main_layout = QVBoxLayout(self)

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = QWidget()

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel(
            f"<b>{label or self.TITLE}</b> ({key})"
        )

        self.remove_btn = QPushButton("✕")
        self.remove_btn.setFixedWidth(28)

        self.remove_btn.setStyleSheet(
            """
            QPushButton{
                color:#e0cb93;
                font-weight:bold;
            }
            """
        )

        header_layout.addWidget(self.title)
        header_layout.addStretch()
        header_layout.addWidget(self.remove_btn)

        self.main_layout.addWidget(header)

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        self.form_container = QWidget()

        self.form_layout = QFormLayout(self.form_container)

        self.form_layout.setFieldGrowthPolicy(
            QFormLayout.ExpandingFieldsGrow
        )

        self.main_layout.addWidget(self.form_container)

        self.build_form()

        self.update_visibility()

    # ---------------------------------------------------------
    # Build UI
    # ---------------------------------------------------------

    def build_form(self):

        self.fields = []

        for definition in self.FIELDS:

            field = self.clone_field(definition)

            widget = field.create_widget()

            label = QLabel(field.label)

            field.widget = widget
            field.label_widget = label
            
            if field.help_text:
                label.setToolTip(
                field.help_text
                )

            widget.setToolTip(
                field.help_text
            )

            # PathSelector is a composite widget. Apply the
            # tooltip to its child widgets as well.
            for child in widget.findChildren(QWidget):
                child.setToolTip(
                    field.help_text
                )
            field.connect(self.change_callback)

            self.form_layout.addRow(
                label,
                widget,
            )

            self.fields.append(field)

        self.connect_visibility_rules()

    # ---------------------------------------------------------

    def clone_field(self, field):
        return field.clone()

    # ---------------------------------------------------------

    def field(self, label):

        for field in self.fields:
            if field.label == label:
                return field

        raise KeyError(label)

    # ---------------------------------------------------------

    def value(self, label):
        return self.field(label).value()

    # ---------------------------------------------------------

    def set_value(
        self,
        label,
        value,
    ):
        self.field(label).set_value(value)

    # ---------------------------------------------------------
    # Visibility
    # ---------------------------------------------------------

    def connect_visibility_rules(self):

        for field in self.fields:

            if field.show_when is None:
                continue

            controller_name, _ = field.show_when

            try:
                controller = self.field(controller_name)

            except KeyError:
                continue

            controller.connect(self.update_visibility)

    # ---------------------------------------------------------

    def update_visibility(self):

        for field in self.fields:

            if field.show_when is None:
                field.set_visible(field.visible)
                continue

            controller_name, expected = field.show_when

            controller = self.field(controller_name)

            visible = controller.value() == expected

            field.set_visible(visible)

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------

    def get_raw_value(self):
        return serialize_fields(self.fields)

    # ---------------------------------------------------------

    def set_raw_value(
        self,
        values,
    ):
        restore_fields(
            self.fields,
            values,
        )

        self.update_visibility()

    # ---------------------------------------------------------
    # Template helpers
    # ---------------------------------------------------------

    @staticmethod
    def comment(enabled, text):
        """
        Returns the text unchanged if enabled=True,
        otherwise returns it commented out.
        """
        return text if enabled else f"# {text}"

    # ---------------------------------------------------------
    # Template
    # ---------------------------------------------------------

    def get_template_context(self):

        context = template_context(self.fields)

        context["KEY"] = self.key

        return context

    # ---------------------------------------------------------

    def render_template(
        self,
        template_root,
        filename,
        context=None,
    ):

        if context is None:
            context = self.get_template_context()

        resolved_filename = filename

        for key, value in context.items():

            resolved_filename = resolved_filename.replace(
                "{{" + key + "}}",
                str(value),
            )

        path = Path(template_root) / resolved_filename

        if not path.exists():
            raise FileNotFoundError(path)

        text = path.read_text(
            encoding="utf-8"
        )

        for key, value in context.items():

            text = text.replace(
                "{{" + key + "}}",
                str(value),
            )

        return text

    # ---------------------------------------------------------
    # Preparation
    # ---------------------------------------------------------

    def prepare_files(self, output_directory):
        """
        Prepare files required by the generated script.

        Subclasses can override this method.
        """
        return {}

    # ---------------------------------------------------------
    # Script Generation
    # ---------------------------------------------------------

    def build_script_fragment(
        self,
        template_root,
        context=None,
    ):

        if self.TEMPLATE is None:
            return ""

        return self.render_template(
            template_root,
            self.TEMPLATE,
            context=context,
        )


    # ---------------------------------------------------------
    # Preview
    # ---------------------------------------------------------

    def get_preview_text(self):
        """
        Returns a human-readable representation of the widget.
        """

        lines = []

        for field in self.fields:

            if field.show_when is not None:
                controller_name, expected = field.show_when

                if self.value(controller_name) != expected:
                    continue

            lines.append(
                f"{field.label}: {field.value()}"
            )

        return "\n".join(lines)

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def values(self):
        """
        Returns a dictionary mapping field labels to values.
        """

        return {
            field.label: field.value()
            for field in self.fields
        }

    # ---------------------------------------------------------

    def template_values(self):
        """
        Returns the template substitution dictionary.
        """

        return self.get_template_context()

    # ---------------------------------------------------------

    def template_value(
        self,
        key,
        default=None,
    ):
        return self.get_template_context().get(
            key,
            default,
        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    def validate(self):
        """
        Override in subclasses if validation is required.

        Returns
        -------
        (bool, str)

            True, ""          -> valid

            False, "message"  -> invalid
        """

        return True, ""

    # ---------------------------------------------------------

    def is_valid(self):
        valid, _ = self.validate()
        return valid

    # ---------------------------------------------------------

    def validation_error(self):
        _, message = self.validate()
        return message

    # ---------------------------------------------------------
    # Iteration helpers
    # ---------------------------------------------------------

    def __iter__(self):
        return iter(self.fields)

    # ---------------------------------------------------------

    def __len__(self):
        return len(self.fields)

    # ---------------------------------------------------------

    def __contains__(self, label):
        return any(
            field.label == label
            for field in self.fields
        )

    # ---------------------------------------------------------

    def __getitem__(self, label):
        return self.field(label)

    # ---------------------------------------------------------

    def __repr__(self):

        return (
            f"<{self.__class__.__name__}"
            f" key={self.key!r}"
            f" fields={len(self.fields)}>"
        )

    # ---------------------------------------------------------
    # Class helpers
    # ---------------------------------------------------------

    @classmethod
    def create(
        cls,
        key,
        label=None,
        change_callback=None,
        parent=None,
        values=None,
    ):
        """
        Convenience factory used by MainWindow when restoring
        widgets from JSON.
        """

        widget = cls(
            key=key,
            label=label,
            change_callback=change_callback,
            parent=parent,
        )

        if values is not None:
            widget.set_raw_value(values)

        return widget

    # ---------------------------------------------------------

    @classmethod
    def registered_types(cls):
        """
        Returns the widget registry.
        """

        return dict(cls.registry)

    # ---------------------------------------------------------

    @classmethod
    def from_type(cls, widget_type):
        """
        Look up a registered widget class.
        """

        return cls.registry.get(widget_type)

    # ---------------------------------------------------------

    @classmethod
    def display_name(cls):
        return cls.TITLE

    # ---------------------------------------------------------

    @classmethod
    def widget_type(cls):
        return cls.TYPE

    # ---------------------------------------------------------

    @classmethod
    def has_template(cls):
        return cls.TEMPLATE is not None

    # ---------------------------------------------------------

    @classmethod
    def field_labels(cls):
        return [
            field.label
            for field in cls.FIELDS
        ]

    # ---------------------------------------------------------

    @classmethod
    def template_variables(cls):
        return [
            field.template
            for field in cls.FIELDS
        ]