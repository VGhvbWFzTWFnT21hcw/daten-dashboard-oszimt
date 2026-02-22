from shiny import ui
import shiny.experimental as x
from shinywidgets import output_widget
import faicons
from datetime import datetime


# Constants
COLORS = {
    "renewable": "#2ECC71", "conventional": "#E74C3C", "demand": "#3498DB",
    "solar": "#F1C40F", "wind": "#1ABC9C", "hydro": "#5DADE2",
    "biomass": "#27AE60", "coal": "#7F8C8D", "gas": "#E67E22", "nuclear": "#9B59B6",
}

# Month mapping for display
MONTH_OPTIONS = {
    0: "Alle Monate",
    1: "Januar", 2: "Februar", 3: "März", 4: "April",
    5: "Mai", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "Dezember"
}

# UI Definition
app_ui = ui.page_fillable(
    ui.page_navbar(
        ui.nav_panel(
            "Übersicht",
            ui.row(
                ui.layout_columns(
                    ui.value_box(title="Ø Tägliche Erzeugung", showcase=faicons.icon_svg("bolt", width="50px"), value=ui.output_text("kpi_avg_generation")),
                    ui.value_box(title="Ø Erneuerbarer Anteil", showcase=faicons.icon_svg("leaf", width="50px"), value=ui.output_text("kpi_renewable_share")),
                    ui.value_box(title="Ø Täglicher Verbrauch", showcase=faicons.icon_svg("plug", width="50px"), value=ui.output_text("kpi_avg_demand")),
                    ui.value_box(title="Ø Sonnenstunden/Tag", showcase=faicons.icon_svg("sun", width="50px"), value=ui.output_text("kpi_sunshine")),
                    col_widths=(3, 3, 3, 3),
                ),
            ),
            ui.row(
                ui.layout_columns(
                    x.ui.card(ui.card_header("Energiemix - Erneuerbar vs. Konventionell"), output_widget("plot_energy_mix")),
                    x.ui.card(ui.card_header("Erzeugung nach Energiequelle"), output_widget("plot_source_breakdown")),
                    col_widths=(5, 7),
                ),
            ),
            ui.row(ui.layout_columns(x.ui.card(ui.card_header("Monatliche Entwicklung"), output_widget("plot_monthly_trend")), col_widths=(12,))),
        ),
        ui.nav_panel(
            "Zeitreihen",
            ui.row(ui.layout_columns(x.ui.card(ui.card_header("Erzeugung und Verbrauch im Zeitverlauf"), output_widget("plot_timeseries"), full_screen=True), col_widths=(12,))),
            ui.row(ui.layout_columns(x.ui.card(ui.card_header("Erneuerbare Erzeugung nach Typ"), output_widget("plot_renewable_timeseries"), full_screen=True), col_widths=(12,))),
        ),
        ui.nav_panel(
            "Tagesprofile",
            ui.row(ui.layout_columns(x.ui.card(ui.card_header("Durchschnittliches Tagesprofil"), output_widget("plot_daily_profile")), x.ui.card(ui.card_header("Tagesprofil nach Wochentag"), output_widget("plot_weekday_profile")), col_widths=(6, 6))),
            ui.row(ui.layout_columns(x.ui.card(ui.card_header("PV-Erzeugung vs. Sonnenschein"), output_widget("plot_solar_correlation")), col_widths=(12,))),
        ),
        ui.nav_panel(
            "Prognose",
            ui.row(ui.layout_columns(x.ui.card(ui.card_header("7-Tage Verbrauchsprognose"), output_widget("plot_forecast"), full_screen=True), col_widths=(12,))),
            ui.row(ui.layout_columns(x.ui.card(ui.card_header("Prognose-Kennzahlen"), ui.output_ui("forecast_metrics")), col_widths=(12,))),
        ),
        title=ui.span("Energie-Dashboard", style="font-weight: bold; color: #2ECC71;"),
        id="page",
        sidebar=ui.sidebar(
            ui.input_date_range(id="date_range", label="Zeitraum auswählen", start="2023-01-01", end="2023-12-31", language="de"),
            # month picker
            ui.input_select(
                id="month_filter",
                label="Monat filtern",
                choices=MONTH_OPTIONS,
                selected=0  # Default to "Alle Monate"
            ),
            ui.input_dark_mode(id="dark_mode", mode="light"),
            open="closed",
        ),
        footer=ui.h6(f"OSZ IMT Berlin - Energiedaten Dashboard © {datetime.now().year}", style="color: white !important; text-align: center;"),
        window_title="Energie-Dashboard OSZ IMT",
    ),
    ui.tags.style(".value-box .value-box-value { font-size: 1.8rem; } .card-header { font-weight: bold; }"),
)
