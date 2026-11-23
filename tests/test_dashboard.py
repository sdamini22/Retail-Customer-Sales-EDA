from pathlib import Path
import ast

APP = Path(__file__).resolve().parents[1] / "app.py"

def test_app_syntax():
    ast.parse(APP.read_text(encoding="utf-8"))

def test_csv_uploader_exists():
    assert "file_uploader" in APP.read_text(encoding="utf-8")

def test_dashboard_has_quality_section():
    assert "Data Quality" in APP.read_text(encoding="utf-8")

def test_dashboard_has_download():
    assert "download_button" in APP.read_text(encoding="utf-8")
