import customtkinter as ctk
from typing import List, Dict
from src.com.themes.ThemeManager import ThemeManager
from src.com.components.buttons import PrimaryBtn


class FormField:

    def __init__(self, field_type, label, required=False, options=None):
        self.field_type = field_type
        self.label = label
        self.required = required
        self.options = options or {}
        self.widget = None
        self.error_label = None
        self.container = None
    
    def validate(self, value):
        if self.required and not value:
            return f"{self.label} is required"
        if self.field_type == "integer":
            if not value.isdigit():
                return f"{self.label} must be a number"
        return None


class Form(ctk.CTkFrame):
    def __init__(self, master, theme, fields: List[Dict], **kwargs):
        super().__init__(master, **kwargs)
        self.form_title = kwargs.get("form_title", "BeingUI Form")
        self.form_submit_text = kwargs.get("form_submit_text", "Submit Form")
        self.theme = theme
        self.configure(fg_color=self.theme.colors.BACKGROUND)
        self.fields = []
        self.data = {}
        self.current_row = 0
        self.create_header()
        self.create_fields(fields)
        self.create_submit_button()
        self.success_label = None

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=self.theme.colors.Modals.BACKGROUND, height=80, corner_radius=0)
        header_frame.grid(row=self.current_row, column=0, columnspan=2, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(header_frame,
                             text=self.form_title,
                             font=("Segoe UI", 24, "bold"),
                             text_color=self.theme.colors.Modals.HEADER)
        title.grid(row=0, column=0, pady=15)
        self.current_row += 1
    
    def create_fields(self, fields_config):
        fields_frame = ctk.CTkFrame(self, fg_color="transparent")
        fields_frame.grid(row=self.current_row, column=0, padx=40, pady=20, sticky="nsew")

        for idx, config in enumerate(fields_config):
            field = FormField(
                field_type=config["type"],
                label=config["label"],
                required=config.get("required", False),
                options=config.get("options", {})
            )
            self.create_field_widgets(fields_frame, field, idx)
            self.fields.append(field)
    
    def create_field_widgets(self, master, field, row_idx):
        field.container = ctk.CTkFrame(master, fg_color="transparent")
        field.container.grid(row=row_idx, column=0, pady=10, padx=10, sticky="ew")

        label = ctk.CTkLabel(field.container,
                             text=field.label + (" *" if field.required else ""),
                             font=("Segoe UI", 12),
                             anchor="w",
                             text_color="#2D3748")
        label.grid(row=0, column=0, padx=(0, 15), sticky="w")

        # Input container with subtle shadow effect
        input_container = ctk.CTkFrame(field.container,
                                       fg_color=self.theme.colors.Modals.BACKGROUND,
                                       corner_radius=8,
                                       border_width=1,
                                       border_color=self.theme.colors.Modals.BORDER)
        input_container.grid(row=0, column=1, sticky="ew", padx=20, pady=10)

        # Create input widget
        if field.field_type in ["string", "integer"]:
            widget = ctk.CTkEntry(input_container,
                                  border_width=0,
                                  fg_color="transparent",
                                  font=("Segoe UI", 12),
                                  height=34)
            widget.pack(padx=10, pady=2, fill="x")
        elif field.field_type == "boolean":
            widget = ctk.CTkCheckBox(input_container,
                                     text="",
                                     checkbox_width=18,
                                     checkbox_height=18,
                                     border_width=1)
            widget.pack(padx=10, pady=6)
        elif field.field_type == "choice":
            widget = ctk.CTkComboBox(input_container,
                                     values=field.options.get("choices", []),
                                     button_color=self.theme.colors.Buttons.PRIMARY,
                                     border_width=0,
                                     dropdown_font=("Segoe UI", 12),
                                     corner_radius=6)
            widget.pack(padx=5, pady=2, fill="x")

        field.widget = widget

        # Error message label
        field.error_label = ctk.CTkLabel(field.container,
                                         text="",
                                         text_color=self.theme.colors.Texts.ERROR,
                                         font=("Segoe UI", 10),
                                         anchor="w")
        field.error_label.grid(row=1, column=1, sticky="w", pady=(2, 0))

        if hasattr(widget, "bind"):
            widget.bind("<Enter>", lambda e, w=input_container: w.configure(fg_color="#EDF2F7"))
            widget.bind("<Leave>", lambda e, w=input_container: w.configure(fg_color="#F7FAFC"))
    
    def create_submit_button(self):
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=self.current_row + 1, column=0, pady=20, sticky="ew")

        self.submit_btn = PrimaryBtn(btn_frame,
                                        text=self.form_submit_text,
                                        command=self.on_submit,
                                        font=("Segoe UI", 14, "bold"))
        self.submit_btn.pack(pady=10, ipadx=30)
    
    def on_submit(self):
        self.data = {}
        errors = False

        for field in self.fields:
            value = self.get_widget_value(field.widget)
            error = field.validate(value)

            if error:
                self.show_error(field, error)
                errors = True
            else:
                self.clear_error(field)
                self.data[field.label] = self.convert_value(field, value)

        if not errors:
            self.show_success()
            print("Form data:", self.data)

    def get_widget_value(self, widget):
        if isinstance(widget, ctk.CTkEntry):
            return widget.get()
        elif isinstance(widget, ctk.CTkCheckBox):
            return widget.get()
        elif isinstance(widget, ctk.CTkComboBox):
            return widget.get()
        return ""

    def convert_value(self, field, value):
        if field.field_type == "integer":
            return int(value) if value else None
        elif field.field_type == "boolean":
            return bool(value)
        return value

    def show_error(self, field, message):
        field.error_label.configure(text=message)
        field.container.configure(fg_color=self.theme.colors.Modals.BACKGROUND)
        field.container.after(2000, lambda: field.container.configure(fg_color="transparent"))

    def clear_error(self, field):
        field.error_label.configure(text="")

    def show_success(self):
        if self.success_label:
            self.success_label.destroy()

        self.success_label = ctk.CTkLabel(self,
                                          text="✓ Form submitted successfully!",
                                          text_color=self.theme.colors.Texts.SUCCESS,
                                          font=("Segoe UI", 12, "bold"))
        self.success_label.grid(row=self.current_row + 2, column=0, pady=15)
        self.after(3000, self.success_label.destroy)


"""
    form_config = [
        {"type": "string", "label": "Full Name", "required": True},
        {"type": "integer", "label": "Age", "required": True},
        {"type": "choice", "label": "Country",
         "options": {"choices": ["USA", "Canada", "UK", "Australia"]}},
        {"type": "boolean", "label": "Subscribe to newsletter"}
    ]
"""