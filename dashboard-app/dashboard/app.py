from shiny import App
from pathlib import Path
from ui import app_ui
from server import server


static_dir = Path(__file__).parent / "static"
app = App(app_ui, server, static_assets=static_dir)
