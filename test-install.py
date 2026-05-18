"""
Run import checks:   python test-install.py
Run as Shiny app:    shiny run test-install.py
"""

import importlib
import os
import sys

PACKAGES = {
    # Core code examples
    "palmerpenguins": "palmerpenguins",
    "plotnine": "plotnine",
    "shiny": "shiny",
    # Website rendering
    "ipykernel": "ipykernel",
    "jupyter": "jupyter_core",
    "shinylive": "shinylive",
    # AI slides (07-08)
    "anthropic": "anthropic",
    "chatlas": "chatlas",
    "openai": "openai",
    "python-dotenv": "dotenv",
    "querychat": "querychat",
    "shinychat": "shinychat",
    # Extended Shiny UI
    "faicons": "faicons",
    "shinywidgets": "shinywidgets",
    # Data & visualization
    "pandas": "pandas",
    "plotly": "plotly",
    "seaborn": "seaborn",
    # Testing
    "playwright": "playwright",
}


def check_imports():
    passed, failed = [], []
    for pkg, import_name in PACKAGES.items():
        try:
            importlib.import_module(import_name)
            passed.append(pkg)
        except ImportError:
            failed.append(pkg)
    return passed, failed


def check_chromium():
    """Check whether Playwright's Chromium browser is installed."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            return os.path.exists(p.chromium.executable_path)
    except Exception:
        return False


if __name__ == "__main__":
    passed, failed = [], []
    print("Checking packages...\n")
    for i, (pkg, import_name) in enumerate(PACKAGES.items(), 1):
        print(f"  [{i:2}/{len(PACKAGES)}] {pkg:<20}", end="", flush=True)
        try:
            importlib.import_module(import_name)
            passed.append(pkg)
            print("✓")
        except ImportError:
            failed.append(pkg)
            print("✗")
    print(f"\n{len(passed)}/{len(PACKAGES)} packages OK")

    print("\nChecking Playwright browser...\n")
    chromium_ok = check_chromium()
    print(f"  chromium             {'✓' if chromium_ok else '✗'}")

    if failed or not chromium_ok:
        if failed:
            print(f"\nFailed: {', '.join(failed)}")
            print("Try: pip install -r requirements.txt")
        if not chromium_ok:
            print("\nChromium browser not installed.")
            print("Try: playwright install chromium")
        sys.exit(1)
    print("\nAll good! Now run: shiny run test-install.py")
    sys.exit(0)


# ── Shiny app ──────────────────────────────────────────────────────────────────
from shiny.express import ui, render

_passed, _failed = check_imports()
_chromium_ok = check_chromium()

ui.page_opts(title="This is a Shiny application test")

with ui.card():
    ui.card_header("Package Status")

    @render.ui
    def pkg_status():
        rows = []
        for pkg in _passed:
            rows.append(ui.tags.div(
                ui.tags.span("✓ ", style="color: #25C8EB;"),
                ui.tags.code(pkg),
            ))
        for pkg in _failed:
            rows.append(ui.tags.div(
                ui.tags.span("✗ ", style="color: #D47454;"),
                ui.tags.code(pkg),
            ))
        summary = f"{len(_passed)}/{len(PACKAGES)} packages OK"
        return ui.tags.div(ui.tags.p(ui.tags.strong(summary)), *rows)

with ui.card():
    ui.card_header("Playwright Browser")

    @render.ui
    def browser_status():
        if _chromium_ok:
            return ui.tags.div(
                ui.tags.span("✓ ", style="color: #25C8EB;"),
                ui.tags.code("chromium"),
            )
        return ui.tags.div(
            ui.tags.div(
                ui.tags.span("✗ ", style="color: #D47454;"),
                ui.tags.code("chromium"),
            ),
            ui.tags.p("Run: ", ui.tags.code("playwright install chromium")),
        )
