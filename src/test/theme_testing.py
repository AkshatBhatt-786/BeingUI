import customtkinter as ctk
from src.com.themes.ThemeManager import ThemeManager


theme_manager = ThemeManager(palette="chocolate")
Colors = theme_manager.colors


class ThemeDemo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pastel Theme Demo")
        self.geometry("1200x800")
        self.configure(fg_color=Colors.BACKGROUND)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()

        # Create main content area
        self.main_frame = ctk.CTkFrame(self, fg_color=Colors.SURFACE)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Add demo components
        self.create_buttons_section()
        self.create_inputs_section()
        self.create_cards_section()
        self.create_status_indicators()
        self.create_modal_button()

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, fg_color=Colors.Sidebar.BACKGROUND,
                               border_color=Colors.Sidebar.BORDER, border_width=1)
        sidebar.grid(row=0, column=0, sticky="nsew")

        label = ctk.CTkLabel(sidebar, text="Sidebar",
                             text_color=Colors.Texts.HEADERS)
        label.pack(pady=20)

        nav_buttons = [
            ("Dashboard", Colors.ACCENT),
            ("Analytics", Colors.SECONDARY),
            ("Settings", Colors.PRIMARY)
        ]

        for text, color in nav_buttons:
            btn = ctk.CTkButton(sidebar, text=text, fg_color=color,
                                hover_color=Colors.Buttons.PRIMARY_HOVER,
                                text_color=Colors.Buttons.TEXT)
            btn.pack(pady=5, padx=10, fill="x")

    def create_buttons_section(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(pady=10, fill="x", padx=20)

        ctk.CTkLabel(frame, text="Buttons", text_color=Colors.Texts.HEADERS).pack(anchor="w")

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        buttons = [
            ("Primary", Colors.Buttons.PRIMARY, Colors.Buttons.PRIMARY_HOVER),
            ("Secondary", Colors.Buttons.SECONDARY, Colors.Buttons.SECONDARY_HOVER),
            ("Accent", Colors.Buttons.ACCENT, Colors.Buttons.ACCENT_HOVER),
            ("Disabled", Colors.Buttons.DISABLED, Colors.Buttons.DISABLED)
        ]

        for text, bg, hover in buttons:
            btn = ctk.CTkButton(btn_frame, text=text, fg_color=bg,
                                hover_color=hover, text_color=Colors.Buttons.TEXT,
                                state="disabled" if "Disabled" in text else "normal")
            btn.pack(side="left", padx=5)

    def create_inputs_section(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(pady=20, fill="x", padx=20)

        ctk.CTkLabel(frame, text="Input Fields", text_color=Colors.Texts.HEADERS).pack(anchor="w")

        input_frame = ctk.CTkFrame(frame, fg_color=Colors.Inputs.BACKGROUND,
                                   border_color=Colors.Inputs.BORDER, border_width=1)
        input_frame.pack(pady=10, fill="x")

        entries = [
            ("Normal Input", Colors.Inputs.TEXT),
            ("Placeholder", Colors.Inputs.PLACEHOLDER),
            ("Error State", Colors.Texts.ERROR)
        ]

        for text, color in entries:
            entry = ctk.CTkEntry(input_frame, placeholder_text=text,
                                 text_color=color, fg_color="transparent",
                                 border_width=0)
            entry.pack(pady=5, fill="x", padx=10)
            if "Error" in text:
                entry.configure(border_color=Colors.Borders.ERROR, border_width=1)

    def create_cards_section(self):
        card_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        card_frame.pack(pady=20, fill="x", padx=20)

        cards = [
            ("Default Card", Colors.Cards.BACKGROUND),
            ("Alt Card", Colors.Cards.ALT_BACKGROUND),
            ("Secondary Card", Colors.Cards.SECONDARY)
        ]

        for text, color in cards:
            card = ctk.CTkFrame(card_frame, fg_color=color,
                                border_color=Colors.Cards.BORDER, border_width=1)
            card.pack(side="left", padx=10, fill="both", expand=True)
            ctk.CTkLabel(card, text=text, text_color=Colors.Texts.PRIMARY).pack(pady=15)

    def create_status_indicators(self):
        frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        frame.pack(pady=20, fill="x", padx=20)

        # Progress bar
        progress = ctk.CTkProgressBar(frame, fg_color=Colors.Cards.BACKGROUND,
                                      progress_color=Colors.SUCCESS)
        progress.pack(pady=5, fill="x")
        progress.set(0.65)

        # Checkbox
        checkbox = ctk.CTkCheckBox(frame, text="Sample Checkbox",
                                   fg_color=Colors.ACCENT, hover_color=Colors.HIGHLIGHT)
        checkbox.pack(pady=10)

        # Switch
        switch = ctk.CTkSwitch(frame, text="Toggle Switch",
                               fg_color=Colors.ACCENT, progress_color=Colors.PRIMARY)
        switch.pack(pady=5)

    def create_modal_button(self):
        btn = ctk.CTkButton(self.main_frame, text="Show Modal",
                            command=self.show_modal,
                            fg_color=Colors.DANGER,
                            hover_color=Colors.WARNING)
        btn.pack(pady=20)

    def show_modal(self):
        modal = ctk.CTkToplevel(self)
        modal.geometry("400x300")
        modal.configure(fg_color=Colors.Modals.BACKGROUND)

        header = ctk.CTkFrame(modal, fg_color=Colors.Modals.HEADER)
        header.pack(fill="x")
        ctk.CTkLabel(header, text="Modal Header", text_color=Colors.Texts.HEADERS).pack(pady=10)

        content = ctk.CTkLabel(modal, text="Modal Content",
                               text_color=Colors.Texts.PRIMARY)
        content.pack(pady=50)


if __name__ == "__main__":
    app = ThemeDemo()
    app.mainloop()