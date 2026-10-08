"""Minimal in-memory stand-in for streamlit so app.py can be exercised without a browser."""
import os, sys, types, contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_PATH = os.path.join(ROOT, "optiarchitect", "app.py")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import pandas as pd

class SS(dict):
    __getattr__ = dict.get
    def __setattr__(self, k, v): self[k] = v

class Fake(types.ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.session_state = SS()
        self.out = []            # all rendered text
        self.pressed = set()
        self.editors = {}
        self.errors = []
        self.query_params = {}
        self.sidebar = self
        self.column_config = types.SimpleNamespace(
            SelectboxColumn=lambda *a, **k: ("sel", a, k), NumberColumn=lambda *a, **k: ("num", a, k))
    def __enter__(self): return self
    def __exit__(self,*a): return False
    def _w(self, *a): self.out.append(" ".join(str(x) for x in a))
    def set_page_config(self, **k): pass
    def markdown(self, t, **k): self._w(t)
    def header(self, t, **k): self._w("#", t)
    def caption(self, t, **k): self._w(t)
    def divider(self): pass
    def code(self, t, **k): self._w(t)
    def table(self, df): self._w(df.to_string())
    def pyplot(self, fig, **k): self._w("<PYPLOT>")
    def write(self, *a): pass
    def download_button(self, label, data, **k): self._w("<DL>", k.get("file_name"))
    @contextlib.contextmanager
    def spinner(self, *a, **k): yield
    @contextlib.contextmanager
    def expander(self, label, **k):
        self._w("<EXP>", label); yield
    @contextlib.contextmanager
    def container(self, **k): yield
    def columns(self, n):
        n = n if isinstance(n, int) else len(n)
        return [self for _ in range(n)]
    def _get(self, key, default):
        if key is None: return default
        if key not in self.session_state: self.session_state[key] = default
        return self.session_state[key]
    def radio(self, label, options, key=None, format_func=str, **k):
        for o in options: format_func(o)
        return self._get(key, options[0])
    def selectbox(self, label, options, key=None, format_func=str, **k):
        for o in options: format_func(o)
        return self._get(key, options[0])
    def checkbox(self, label, value=False, key=None, **k): return self._get(key, value)
    def text_input(self, label, value="", key=None, **k): return self._get(key, value)
    def number_input(self, label, min_value=None, max_value=None, value=None, step=None, key=None, **k):
        return self._get(key, value)
    def data_editor(self, df, key=None, **k): return self.editors.get(key, df)
    def button(self, label, key=None, on_click=None, args=(), disabled=False, **k):
        hit = key in self.pressed and not disabled
        if hit and on_click: on_click(*args)
        return hit

def run(scenario):
    import runpy
    fake = Fake()
    fake.session_state.update(scenario.get("state", {}))
    fake.pressed = set(scenario.get("pressed", ()))
    fake.editors = scenario.get("editors", {})
    sys.modules["streamlit"] = fake
    for m in [m for m in sys.modules if m in ("app",)]: del sys.modules[m]
    runpy.run_path(APP_PATH, run_name="app_under_test")
    return fake


TEXT_OK = {"en": "Completed - solution verified", "ar": "تم التحقق من الحل"}
