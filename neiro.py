import tkinter as tk
from tkinter import font
import math

# ── Palette ──────────────────────────────────────────────────────────────────
BG          = "#0d0d0f"
PANEL       = "#16161a"
GLASS       = "#1e1e26"
GLASS_LIGHT = "#252530"
ACCENT      = "#7f5af0"
ACCENT2     = "#2cb67d"
TEXT_MAIN   = "#fffffe"
TEXT_DIM    = "#94a1b2"
BTN_OP      = "#7f5af0"
BTN_EQ      = "#2cb67d"
BTN_SPEC    = "#252530"
BTN_NUM     = "#1e1e26"
SHADOW      = "#000000"

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._expr      = ""
        self._display   = ""
        self._just_eval = False
        self._history   = []

        self._build_fonts()
        self._build_ui()
        self._animate_in()

    # ── Fonts ─────────────────────────────────────────────────────────────────
    def _build_fonts(self):
        self.f_display  = font.Font(family="JetBrains Mono", size=36, weight="bold")
        self.f_expr     = font.Font(family="JetBrains Mono", size=13)
        self.f_btn      = font.Font(family="JetBrains Mono", size=16, weight="bold")
        self.f_btn_sm   = font.Font(family="JetBrains Mono", size=12)
        self.f_hist     = font.Font(family="JetBrains Mono", size=10)

    # ── UI Layout ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        outer = tk.Frame(self, bg=BG, padx=20, pady=20)
        outer.pack()

        # ── Title bar ─────────────────────────────────────────────────────────
        title_row = tk.Frame(outer, bg=BG)
        title_row.pack(fill="x", pady=(0, 14))
        tk.Label(title_row, text="◈ CALC", bg=BG,
                 fg=ACCENT, font=font.Font(family="JetBrains Mono", size=11, weight="bold")
                 ).pack(side="left")
        tk.Label(title_row, text="v2.0", bg=BG,
                 fg=TEXT_DIM, font=font.Font(family="JetBrains Mono", size=10)
                 ).pack(side="right")

        # ── Display panel ─────────────────────────────────────────────────────
        disp_panel = tk.Frame(outer, bg=GLASS, bd=0,
                              highlightbackground=ACCENT, highlightthickness=1)
        disp_panel.pack(fill="x", pady=(0, 14))

        inner_disp = tk.Frame(disp_panel, bg=GLASS, padx=18, pady=14)
        inner_disp.pack(fill="both")

        # expression line
        self._expr_var = tk.StringVar(value="")
        tk.Label(inner_disp, textvariable=self._expr_var,
                 bg=GLASS, fg=TEXT_DIM, font=self.f_expr,
                 anchor="e", width=22
                 ).pack(fill="x")

        # main number
        self._disp_var = tk.StringVar(value="0")
        self._disp_lbl = tk.Label(inner_disp, textvariable=self._disp_var,
                                  bg=GLASS, fg=TEXT_MAIN, font=self.f_display,
                                  anchor="e", width=14)
        self._disp_lbl.pack(fill="x")

        # accent line
        tk.Frame(inner_disp, bg=ACCENT, height=2).pack(fill="x", pady=(8, 0))

        # history
        self._hist_var = tk.StringVar(value="")
        tk.Label(inner_disp, textvariable=self._hist_var,
                 bg=GLASS, fg=TEXT_DIM, font=self.f_hist,
                 anchor="e", width=22
                 ).pack(fill="x", pady=(4, 0))

        # ── Button grid ───────────────────────────────────────────────────────
        grid = tk.Frame(outer, bg=BG)
        grid.pack()

        layout = [
            # (label, colspan, color, action)
            [("C",   1, BTN_SPEC, "clear"),   ("⌫",   1, BTN_SPEC, "back"),
             ("%",   1, BTN_SPEC, "%"),        ("÷",   1, BTN_OP,   "/")],

            [("7",   1, BTN_NUM,  "7"),        ("8",   1, BTN_NUM,  "8"),
             ("9",   1, BTN_NUM,  "9"),        ("×",   1, BTN_OP,   "*")],

            [("4",   1, BTN_NUM,  "4"),        ("5",   1, BTN_NUM,  "5"),
             ("6",   1, BTN_NUM,  "6"),        ("−",   1, BTN_OP,   "-")],

            [("1",   1, BTN_NUM,  "1"),        ("2",   1, BTN_NUM,  "2"),
             ("3",   1, BTN_NUM,  "3"),        ("+",   1, BTN_OP,   "+")],

            [("±",   1, BTN_SPEC, "negate"),   ("0",   1, BTN_NUM,  "0"),
             (".",   1, BTN_SPEC, "."),        ("=",   1, BTN_EQ,   "=")],
        ]

        GAP = 10
        W, H = 70, 60

        for r, row in enumerate(layout):
            for c, (lbl, span, color, action) in enumerate(row):
                self._make_btn(grid, lbl, color, action, r, c, W, H, GAP)

    # ── Button factory ────────────────────────────────────────────────────────
    def _make_btn(self, parent, text, color, action, row, col, W, H, GAP):
        is_eq = (action == "=")
        is_op = color == BTN_OP

        # shadow frame
        shadow = tk.Frame(parent, bg="#000000",
                          width=W+4, height=H+4)
        shadow.grid(row=row, column=col, padx=GAP//2, pady=GAP//2)
        shadow.grid_propagate(False)

        btn_frame = tk.Frame(shadow, bg=color,
                             width=W, height=H,
                             highlightbackground=
                                 ACCENT if is_op else (ACCENT2 if is_eq else GLASS_LIGHT),
                             highlightthickness=1 if (is_op or is_eq) else 0)
        btn_frame.place(x=1, y=1, width=W, height=H)
        btn_frame.pack_propagate(False)

        lbl = tk.Label(btn_frame, text=text, bg=color,
                       fg=TEXT_MAIN,
                       font=self.f_btn if len(text) == 1 else self.f_btn_sm,
                       cursor="hand2")
        lbl.place(relx=.5, rely=.5, anchor="center")

        # hover + press effects
        def on_enter(e, f=btn_frame, c=color, b=lbl):
            lighter = self._lighten(c)
            f.configure(bg=lighter)
            b.configure(bg=lighter)

        def on_leave(e, f=btn_frame, c=color, b=lbl):
            f.configure(bg=c)
            b.configure(bg=c)

        def on_press(e, f=btn_frame, c=color, b=lbl):
            darker = self._darken(c)
            f.configure(bg=darker)
            b.configure(bg=darker)

        def on_release(e, a=action, f=btn_frame, c=color, b=lbl):
            f.configure(bg=c)
            b.configure(bg=c)
            self._handle(a)

        for w in (btn_frame, lbl):
            w.bind("<Enter>",          on_enter)
            w.bind("<Leave>",          on_leave)
            w.bind("<ButtonPress-1>",  on_press)
            w.bind("<ButtonRelease-1>",on_release)

    # ── Logic ─────────────────────────────────────────────────────────────────
    def _handle(self, action):
        if action == "clear":
            self._expr = ""
            self._disp_var.set("0")
            self._expr_var.set("")
            self._just_eval = False

        elif action == "back":
            if self._just_eval:
                return
            self._expr = self._expr[:-1]
            self._disp_var.set(self._expr or "0")

        elif action == "negate":
            try:
                val = float(self._disp_var.get())
                val = -val
                self._expr = self._fmt(val)
                self._disp_var.set(self._expr)
            except:
                pass

        elif action == "%":
            try:
                val = float(self._expr) / 100
                self._expr = self._fmt(val)
                self._disp_var.set(self._expr)
            except:
                pass

        elif action == "=":
            self._evaluate()

        else:
            if self._just_eval and action not in "+-*/":
                self._expr = ""
            self._just_eval = False
            self._expr += action
            self._disp_var.set(self._expr)
            self._expr_var.set("")

        self._pulse()

    def _evaluate(self):
        if not self._expr:
            return
        try:
            safe_expr = self._expr.replace("^", "**")
            result    = eval(safe_expr, {"__builtins__": {}}, {})
            result    = self._fmt(result)

            entry = f"{self._expr} = {result}"
            self._history.append(entry)
            if len(self._history) > 3:
                self._history.pop(0)
            self._hist_var.set(" │ ".join(self._history[-2:]))

            self._expr_var.set(self._expr + " =")
            self._expr      = result
            self._disp_var.set(result)
            self._just_eval = True
        except:
            self._disp_var.set("Error")
            self._expr      = ""
            self._just_eval = True

    @staticmethod
    def _fmt(val):
        if isinstance(val, float) and val == int(val):
            return str(int(val))
        return str(round(val, 10)).rstrip("0").rstrip(".")

    # ── Helpers ───────────────────────────────────────────────────────────────
    @staticmethod
    def _lighten(hex_color, amount=30):
        hex_color = hex_color.lstrip("#")
        r, g, b   = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        r, g, b   = min(r+amount, 255), min(g+amount, 255), min(b+amount, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def _darken(hex_color, amount=20):
        hex_color = hex_color.lstrip("#")
        r, g, b   = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        r, g, b   = max(r-amount, 0), max(g-amount, 0), max(b-amount, 0)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ── Animations ────────────────────────────────────────────────────────────
    def _pulse(self):
        """Flash the display label accent colour briefly."""
        self._disp_lbl.configure(fg=ACCENT)
        self.after(80, lambda: self._disp_lbl.configure(fg=TEXT_MAIN))

    def _animate_in(self):
        """Fade-in window (Windows/Linux alpha support)."""
        try:
            self.attributes("-alpha", 0.0)
            self._fade(0.0)
        except:
            pass

    def _fade(self, alpha):
        alpha = min(alpha + 0.07, 1.0)
        try:
            self.attributes("-alpha", alpha)
        except:
            return
        if alpha < 1.0:
            self.after(16, lambda: self._fade(alpha))

    # ── Keyboard ──────────────────────────────────────────────────────────────
    def _bind_keys(self):
        mapping = {
            "Return": "=", "KP_Enter": "=",
            "BackSpace": "back", "Escape": "clear",
            "plus": "+", "minus": "-",
            "asterisk": "*", "slash": "/",
            "percent": "%", "period": ".", "comma": ".",
        }
        for k, v in mapping.items():
            self.bind(f"<{k}>", lambda e, a=v: self._handle(a))
        for d in "0123456789":
            self.bind(d, lambda e, a=d: self._handle(a))
            self.bind(f"<KP_{d}>", lambda e, a=d: self._handle(a))


if __name__ == "__main__":
    app = Calculator()
    app._bind_keys()
    app.mainloop()