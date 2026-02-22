from shiny import reactive, render, ui
from shinywidgets import render_widget
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import timedelta
import duckdb
import faicons
from ui import COLORS

def read_energy_data():
    con = duckdb.connect("duckdb/energy_data.duckdb")
    query = "SELECT g.*, t.full_timestamp, t.hour, t.month, t.day, t.weekday FROM fact_generation g LEFT JOIN dim_time t ON g.timestamp = t.full_timestamp"
    df = con.execute(query).df()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["date"] = df["timestamp"].dt.date
    con.close()
    return df

def read_sunshine_data():
    con = duckdb.connect("duckdb/energy_data.duckdb")
    df = con.execute("SELECT timestamp, sunshine_minutes_15min FROM fact_generation").df()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour
    con.close()
    return df

df_energy_full = read_energy_data()
df_sunshine_full = read_sunshine_data()


def get_color_template(mode):
    return "plotly_white" if mode == "light" else "plotly_dark"


def get_background_color(mode):
    return "white" if mode == "light" else "rgb(29, 32, 33)"

def server(input, output, session):
    # Update the date range once the server starts
    ui.update_date_range(
        "date_range",
        start=df_energy_full["date"].min(),
        end=df_energy_full["date"].max(),
        min=df_energy_full["date"].min(),
        max=df_energy_full["date"].max()
    )

    # @reactive.Calc
    # def filtered_energy():
    #     start, end = input.date_range()
    #     mask = (df_energy_full["date"] >= start) & (df_energy_full["date"] <= end)
    #     return df_energy_full[mask]

    # @reactive.Calc
    # def filtered_sunshine():
    #     start, end = input.date_range()
    #     mask = (df_sunshine_full["date"] >= start) & (df_sunshine_full["date"] <= end)
    #     return df_sunshine_full[mask]

    @reactive.Calc
    def filtered_energy():
        df = df_energy_full.copy()

        # 1. Filter by Date Range
        start, end = input.date_range()
        mask = (df["date"] >= start) & (df["date"] <= end)
        df = df[mask]

        # 2. Filter by Month (if not "Alle Monate" / 0)
        selected_month = int(input.month_filter())
        if selected_month != 0:
            # Assuming your dataframe has a 'month' column from the dim_time join
            df = df[df["month"] == selected_month]

        return df

    @reactive.Calc
    def filtered_sunshine():
        df = df_sunshine_full.copy()

        # Apply same logic to sunshine data
        start, end = input.date_range()
        mask = (df["date"] >= start) & (df["date"] <= end)
        df = df[mask]

        selected_month = int(input.month_filter())
        if selected_month != 0:
            # If sunshine doesn't have a month column, extract it from timestamp
            df = df[df["timestamp"].dt.month == selected_month]

        return df

    @reactive.Effect
    @reactive.event(input.month_filter)
    def _update_date_on_month_change():
        month = int(input.month_filter())
        if month != 0:
            # Find the first and last day of that month in your current year
            # Or simply update the start/end to focus on that month
            year = df_energy_full["timestamp"].dt.year.max()
            start_date = f"{year}-{month:02d}-01"
            # This is a simple way to focus the view
            ui.update_date_range("date_range", start=start_date)


    # KPIs mit @render.text
    @render.text
    def kpi_avg_generation():
        df = filtered_energy()
        if df.empty:
            return "-- GWh"
        daily = df.groupby("date")["total_generation_mw"].sum() / 4 / 1000
        return f"{daily.mean():.1f} GWh"

    @render.text
    def kpi_renewable_share():
        df = filtered_energy()
        if df.empty:
            return "-- %"
        return f"{df['renewable_share'].mean():.1f} %"

    @render.text
    def kpi_avg_demand():
        df = filtered_energy()
        if df.empty:
            return "-- GWh"
        daily = df.groupby("date")["demand_mw"].sum() / 4 / 1000
        return f"{daily.mean():.1f} GWh"

    @render.text
    def kpi_sunshine():
        df = filtered_sunshine()
        if df.empty:
            return "-- h"
        daily = df.groupby("date")["sunshine_minutes_15min"].sum() / 60
        return f"{daily.mean():.1f} h"

    # Plot: Energiemix Pie Chart
    @render_widget
    def plot_energy_mix():
        df = filtered_energy()

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        renewable_total = df["renewable_mw"].sum()
        conventional_total = df["conventional_mw"].sum()

        fig = go.Figure(data=[go.Pie(
            labels=["Erneuerbar", "Konventionell"],
            values=[renewable_total, conventional_total],
            hole=0.4,
            marker_colors=[COLORS["renewable"], COLORS["conventional"]],
            textinfo="percent+label",
            textfont_size=14,
        )])

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
        )

        return fig

    # Plot: Aufschlüsselung nach Energiequelle
    @render_widget
    def plot_source_breakdown():
        df = filtered_energy()

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        sources = {
            "Wind Onshore": df["wind_onshore_mw"].sum(),
            "Wind Offshore": df["wind_offshore_mw"].sum(),
            "Photovoltaik": df["photovoltaics_mw"].sum(),
            "Wasserkraft": df["hydro_runofriver_mw"].sum(),
            "Biomasse": df["biomass_mw"].sum(),
            "Braunkohle": df["lignite_mw"].sum(),
            "Steinkohle": df["hard_coal_mw"].sum(),
            "Erdgas": df["fossil_gas_mw"].sum(),
        }

        sources = dict(sorted(sources.items(), key=lambda x: x[1], reverse=True))
        colors = ["#1ABC9C", "#16A085", "#F1C40F", "#5DADE2", "#27AE60", "#7F8C8D", "#95A5A6", "#E67E22"]

        fig = go.Figure(data=[go.Bar(
            x=list(sources.keys()),
            y=[v / 1e6 for v in sources.values()],
            marker_color=colors,
            text=[f"{v/1e6:.1f}" for v in sources.values()],
            textposition="outside",
        )])

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            yaxis_title="Erzeugung (TWh)",
            xaxis_tickangle=-45,
            margin=dict(t=20, b=100, l=60, r=20),
            showlegend=False,
        )

        return fig

    # Plot: Monatliche Entwicklung
    @render_widget
    def plot_monthly_trend():
        df = filtered_energy()

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        monthly = df.groupby("month").agg({
            "renewable_mw": "sum",
            "conventional_mw": "sum",
            "demand_mw": "sum",
        }).reset_index()

        for col in ["renewable_mw", "conventional_mw", "demand_mw"]:
            monthly[col] = monthly[col] / 4 / 1000

        month_names = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
                       "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
        monthly["month_name"] = monthly["month"].apply(lambda x: month_names[x-1])

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name="Erneuerbar",
            x=monthly["month_name"],
            y=monthly["renewable_mw"],
            marker_color=COLORS["renewable"],
        ))

        fig.add_trace(go.Bar(
            name="Konventionell",
            x=monthly["month_name"],
            y=monthly["conventional_mw"],
            marker_color=COLORS["conventional"],
        ))

        fig.add_trace(go.Scatter(
            name="Verbrauch",
            x=monthly["month_name"],
            y=monthly["demand_mw"],
            mode="lines+markers",
            line=dict(color=COLORS["demand"], width=3),
            marker=dict(size=8),
        ))

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            barmode="stack",
            yaxis_title="Energie (GWh)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=60, r=20),
        )

        return fig

    # Plot: Zeitreihe Erzeugung/Verbrauch
    @render_widget
    def plot_timeseries():
        df = filtered_energy()

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        daily = df.groupby("date").agg({
            "total_generation_mw": "mean",
            "demand_mw": "mean",
            "renewable_mw": "mean",
        }).reset_index()

        daily["date"] = daily["date"].astype(str)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name="Gesamterzeugung",
            x=daily["date"],
            y=daily["total_generation_mw"] / 1000,
            mode="lines",
            line=dict(color=COLORS["renewable"], width=1),
            fill="tozeroy",
            fillcolor="rgba(46, 204, 113, 0.3)",
        ))

        fig.add_trace(go.Scatter(
            name="Verbrauch",
            x=daily["date"],
            y=daily["demand_mw"] / 1000,
            mode="lines",
            line=dict(color=COLORS["demand"], width=2),
        ))

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            yaxis_title="Leistung (GW)",
            xaxis_title="Datum",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=60, r=20),
            hovermode="x unified",
        )

        return fig

    # Plot: Erneuerbare Zeitreihe
    @render_widget
    def plot_renewable_timeseries():
        df = filtered_energy()

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        daily = df.groupby("date").agg({
            "wind_onshore_mw": "mean",
            "wind_offshore_mw": "mean",
            "photovoltaics_mw": "mean",
        }).reset_index()

        daily["date"] = daily["date"].astype(str)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name="Wind Onshore",
            x=daily["date"],
            y=daily["wind_onshore_mw"] / 1000,
            mode="lines",
            stackgroup="one",
            line=dict(color="#1ABC9C"),
        ))

        fig.add_trace(go.Scatter(
            name="Wind Offshore",
            x=daily["date"],
            y=daily["wind_offshore_mw"] / 1000,
            mode="lines",
            stackgroup="one",
            line=dict(color="#16A085"),
        ))

        fig.add_trace(go.Scatter(
            name="Photovoltaik",
            x=daily["date"],
            y=daily["photovoltaics_mw"] / 1000,
            mode="lines",
            stackgroup="one",
            line=dict(color=COLORS["solar"]),
        ))

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            yaxis_title="Leistung (GW)",
            xaxis_title="Datum",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=60, r=20),
            hovermode="x unified",
        )

        return fig

    # Plot: Tagesprofil
    @render_widget
    def plot_daily_profile():
        df = filtered_energy()

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        hourly = df.groupby("hour").agg({
            "demand_mw": "mean",
            "renewable_mw": "mean",
            "photovoltaics_mw": "mean",
        }).reset_index()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name="Verbrauch",
            x=hourly["hour"],
            y=hourly["demand_mw"] / 1000,
            mode="lines+markers",
            line=dict(color=COLORS["demand"], width=3),
        ))

        fig.add_trace(go.Scatter(
            name="Erneuerbare",
            x=hourly["hour"],
            y=hourly["renewable_mw"] / 1000,
            mode="lines+markers",
            line=dict(color=COLORS["renewable"], width=3),
        ))

        fig.add_trace(go.Scatter(
            name="Photovoltaik",
            x=hourly["hour"],
            y=hourly["photovoltaics_mw"] / 1000,
            mode="lines+markers",
            line=dict(color=COLORS["solar"], width=2, dash="dash"),
        ))

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            yaxis_title="Leistung (GW)",
            xaxis_title="Stunde",
            xaxis=dict(tickmode="linear", tick0=0, dtick=2),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=60, r=20),
        )

        return fig

    # Plot: Wochentag-Profil
    @render_widget
    def plot_weekday_profile():
        df = filtered_energy()

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        weekday_names = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

        weekday = df.groupby("weekday").agg({
            "demand_mw": "mean",
        }).reset_index()
        weekday["weekday_name"] = weekday["weekday"].apply(lambda x: weekday_names[x])

        fig = go.Figure(data=[go.Bar(
            x=weekday["weekday_name"],
            y=weekday["demand_mw"] / 1000,
            marker_color=COLORS["demand"],
            text=[f"{v/1000:.1f}" for v in weekday["demand_mw"]],
            textposition="outside",
        )])

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            yaxis_title="Ø Verbrauch (GW)",
            margin=dict(t=20, b=40, l=60, r=20),
        )

        return fig

    # Plot: Solar-Korrelation
    @render_widget
    def plot_solar_correlation():
        df_e = filtered_energy()
        df_s = filtered_sunshine()

        if df_e.empty or df_s.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        merged = pd.merge(
            df_e[["timestamp", "photovoltaics_mw"]],
            df_s[["timestamp", "sunshine_minutes_15min"]],
            on="timestamp",
            how="inner"
        )

        merged["hour"] = pd.to_datetime(merged["timestamp"]).dt.hour
        hourly = merged.groupby("hour").agg({
            "photovoltaics_mw": "mean",
            "sunshine_minutes_15min": "mean",
        }).reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Bar(
                name="PV-Erzeugung",
                x=hourly["hour"],
                y=hourly["photovoltaics_mw"] / 1000,
                marker_color=COLORS["solar"],
                opacity=0.7,
            ),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(
                name="Sonnenschein",
                x=hourly["hour"],
                y=hourly["sunshine_minutes_15min"],
                mode="lines+markers",
                line=dict(color="#E74C3C", width=3),
                marker=dict(size=8),
            ),
            secondary_y=True,
        )

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            xaxis_title="Stunde",
            xaxis=dict(tickmode="linear", tick0=0, dtick=2),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=60, r=60),
        )

        fig.update_yaxes(title_text="PV-Erzeugung (GW)", secondary_y=False)
        fig.update_yaxes(title_text="Sonnenschein (min/15min)", secondary_y=True)

        return fig

    # Plot: Prognose
    @render_widget
    def plot_forecast():
        df = filtered_energy()

        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="Keine Daten", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return fig

        daily = df.groupby("date").agg({
            "demand_mw": "sum",
        }).reset_index()
        daily["demand_gwh"] = daily["demand_mw"] / 4 / 1000
        daily["date"] = pd.to_datetime(daily["date"])

        daily["ma7"] = daily["demand_gwh"].rolling(window=7).mean()

        if len(daily) >= 7:
            last_7_days = daily.tail(7)
            trend = (last_7_days["demand_gwh"].iloc[-1] - last_7_days["demand_gwh"].iloc[0]) / 7
            forecast_dates = pd.date_range(start=daily["date"].max() + timedelta(days=1), periods=7)
            forecast_values = [daily["ma7"].iloc[-1] + trend * (i+1) for i in range(7)]
        else:
            forecast_dates = []
            forecast_values = []

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            name="Täglicher Verbrauch",
            x=daily["date"],
            y=daily["demand_gwh"],
            mode="lines",
            line=dict(color=COLORS["demand"], width=1),
            opacity=0.5,
        ))

        fig.add_trace(go.Scatter(
            name="7-Tage Durchschnitt",
            x=daily["date"],
            y=daily["ma7"],
            mode="lines",
            line=dict(color=COLORS["renewable"], width=3),
        ))

        if len(forecast_dates) > 0:
            fig.add_trace(go.Scatter(
                name="Prognose",
                x=forecast_dates,
                y=forecast_values,
                mode="lines+markers",
                line=dict(color="#E74C3C", width=3, dash="dash"),
                marker=dict(size=10),
            ))

        fig.update_layout(
            template=get_color_template(input.dark_mode()),
            paper_bgcolor=get_background_color(input.dark_mode()),
            yaxis_title="Verbrauch (GWh/Tag)",
            xaxis_title="Datum",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=40, b=40, l=60, r=20),
            hovermode="x unified",
        )

        return fig

    # Prognose-Metriken
    @render.ui
    def forecast_metrics():
        df = filtered_energy()

        if df.empty:
            return ui.div("Keine Daten verfügbar")

        daily = df.groupby("date").agg({
            "demand_mw": "sum",
        }).reset_index()
        daily["demand_gwh"] = daily["demand_mw"] / 4 / 1000

        avg = daily["demand_gwh"].mean()
        std = daily["demand_gwh"].std()
        trend = (daily["demand_gwh"].iloc[-1] - daily["demand_gwh"].iloc[0]) / len(daily) if len(daily) > 1 else 0

        return ui.div(
            ui.row(
                ui.layout_columns(
                    ui.value_box(
                        title="Ø Tagesverbrauch",
                        value=f"{avg:.1f} GWh",
                        showcase=faicons.icon_svg("chart-line", width="30px"),
                    ),
                    ui.value_box(
                        title="Standardabweichung",
                        value=f"± {std:.1f} GWh",
                        showcase=faicons.icon_svg("arrows-left-right", width="30px"),
                    ),
                    ui.value_box(
                        title="Trend",
                        value=f"{'+' if trend > 0 else ''}{trend:.2f} GWh/Tag",
                        showcase=faicons.icon_svg("arrow-trend-up" if trend > 0 else "arrow-trend-down", width="30px"),
                    ),
                    col_widths=(4, 4, 4),
                ),
            ),
        )
