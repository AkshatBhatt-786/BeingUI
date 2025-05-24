import customtkinter as ctk
from typing import Optional, Any
from dataclasses import dataclass
from src.com.themes.ThemeManager import ThemeManager
from typing import Tuple


@dataclass
class ButtonColors:
    PRIMARY: str
    PRIMARY_HOVER: str
    SECONDARY: str
    SECONDARY_HOVER: str
    ACCENT: str
    ACCENT_HOVER: str
    DISABLED: str
    TEXT: str

class AnimatedBaseButton(ctk.CTkButton):

    def __init__(self, master: any,
                 theme_manager: Optional[object] = None,
                 width: int = 180,
                 height: int = 50,
                 animation_duration: int = 300,
                 **kwargs):

        self.theme_manager = theme_manager
        self.animation_duration = animation_duration
        self.is_hovered = False
        self.anim_id = None

        super().__init__(
            master=master,
            width=width,
            height=height,
            **kwargs
        )

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _get_color(self, color_path: str) -> str:
        """Safely get color from theme manager"""
        if self.theme_manager:
            parts = color_path.split('.')
            color_obj = self.theme_manager.colors
            for part in parts:
                color_obj = getattr(color_obj, part, None)
                if not color_obj: break
            return color_obj if isinstance(color_obj, str) else "#FFFFFF"
        return "#FFFFFF"

    def _animate_property(self, start: float, end: float,
                          callback: callable, duration: int = None):
        duration = duration or self.animation_duration
        start_time = time.time()

        def update():
            nonlocal start_time
            elapsed = (time.time() - start_time) * 1000
            progress = min(elapsed / duration, 1.0)
            current = start + (end - start) * progress
            callback(current)

            if progress < 1.0:
                self.anim_id = self.after(16, update)
            else:
                self.anim_id = None

        self.after(0, update)

    def _on_enter(self, event=None):
        self.is_hovered = True

    def _on_leave(self, event=None):
        self.is_hovered = False

    def update_theme(self, theme_manager):
        self.theme_manager = theme_manager
        self.configure(
            fg_color=self._get_color('Buttons.PRIMARY'),
            hover_color=self._get_color('Buttons.PRIMARY_HOVER'),
            text_color=self._get_color('Buttons.TEXT')
        )




class BaseButton(ctk.CTkButton):
    def __init__(
            self,
            master: Any,
            theme_manager: Optional[Any] = None,
            text: str = "Button",
            width: int = 150,
            height: int = 42,
            border_width: int = 2,
            **kwargs
    ):
        self.theme_manager = theme_manager
        self._colors = self._get_button_colors()

        super().__init__(
            master=master,
            text=text,
            width=width,
            height=height,
            border_width=border_width,
            **self._base_kwargs(),
            **kwargs
        )

    def _get_button_colors(self) -> ButtonColors:
        if self.theme_manager and hasattr(self.theme_manager, 'colors'):
            buttons = getattr(self.theme_manager.colors, 'Buttons', None)
            return ButtonColors(
                PRIMARY=getattr(buttons, 'PRIMARY', '#6750A4'),
                PRIMARY_HOVER=getattr(buttons, 'PRIMARY_HOVER', '#7C6DAF'),
                SECONDARY=getattr(buttons, 'SECONDARY', '#E8E0FF'),
                SECONDARY_HOVER=getattr(buttons, 'SECONDARY_HOVER', '#D0C4ED'),
                ACCENT=getattr(buttons, 'ACCENT', '#E8E0FF'),
                ACCENT_HOVER=getattr(buttons, 'ACCENT_HOVER', '#D0C4ED'),
                DISABLED=getattr(buttons, 'DISABLED', '#E0E0E0'),
                TEXT=getattr(buttons, 'TEXT', '#FFFFFF')
            )
        return ButtonColors(
            PRIMARY='#6750A4',
            PRIMARY_HOVER='#7C6DAF',
            SECONDARY='#E8E0FF',
            SECONDARY_HOVER='#D0C4ED',
            ACCENT='#E8E0FF',
            ACCENT_HOVER='#D0C4ED',
            DISABLED='#E0E0E0',
            TEXT='#FFFFFF'
        )

    def _base_kwargs(self) -> dict:
        return {
            'corner_radius': 8,
            'text_color': self._colors.TEXT,
            'border_color': self._colors.ACCENT
        }

    def update_theme(self, theme_manager: Any) -> None:
        self.theme_manager = theme_manager
        self._colors = self._get_button_colots()
        self.configure(
            text_color=self._colors.TEXT,
            border_color=self._colors.ACCENT
        )


class PrimaryBtn(BaseButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            fg_color=self._colors.PRIMARY,
            hover_color=self._colors.PRIMARY_HOVER
        )

    def update_theme(self, theme_manager: Any) -> None:
        super().update_theme(theme_manager)
        self.configure(
            fg_color=self._colors.PRIMARY,
            hover_color=self._colors.PRIMARY_HOVER
        )


class SecondaryBtn(BaseButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            fg_color=self._colors.SECONDARY,
            hover_color=self._colors.SECONDARY_HOVER
        )

    def update_theme(self, theme_manager: Any) -> None:
        super().update_theme(theme_manager)
        self.configure(
            fg_color=self._colors.SECONDARY,
            hover_color=self._colors.SECONDARY_HOVER
        )


class RectangularBtn(PrimaryBtn):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(corner_radius=0)


class OutlinedBtn(BaseButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            fg_color='transparent',
            hover_color=self._colors.SECONDARY,
            text_color=self._colors.PRIMARY,
            border_color=self._colors.PRIMARY
        )

    def update_theme(self, theme_manager: Any) -> None:
        super().update_theme(theme_manager)
        self.configure(
            text_color=self._colors.PRIMARY,
            border_color=self._colors.PRIMARY,
            hover_color=self._colors.SECONDARY
        )


class GradientButton(AnimatedBaseButton):

    def __init__(self, master: any,
                 gradient: Tuple[str, str] = ("#6D4C41", "#D2691E"),
                 **kwargs):
        super().__init__(master, **kwargs)
        self.gradient = gradient
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        w = self.winfo_width()
        h = self.winfo_height()
        self.canvas.delete("gradient")

        for i in range(h):
            ratio = i / h
            r = int((1 - ratio) * int(self.gradient[0][1:3], 16) + ratio * int(self.gradient[1][1:3], 16))
            g = int((1 - ratio) * int(self.gradient[0][3:5], 16) + ratio * int(self.gradient[1][3:5], 16))
            b = int((1 - ratio) * int(self.gradient[0][5:7], 16) + ratio * int(self.gradient[1][5:7], 16))
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, w, i, tags=("gradient",), fill=color)

    def _on_enter(self, event):
        super()._on_enter(event)
        self._animate_property(0, 1, lambda v: setattr(self, 'gradient', (
            self._interpolate_color("#6D4C41", "#FFD700", v),
            self._interpolate_color("#D2691E", "#FFA726", v)
        )) and self._draw_gradient())

    def _interpolate_color(self, start: str, end: str, ratio: float) -> str:
        r = int((1 - ratio) * int(start[1:3], 16) + ratio * int(end[1:3], 16))
        g = int((1 - ratio) * int(start[3:5], 16) + ratio * int(end[3:5], 16))
        b = int((1 - ratio) * int(start[5:7], 16) + ratio * int(end[5:7], 16))
        return f"#{r:02x}{g:02x}{b:02x}"

