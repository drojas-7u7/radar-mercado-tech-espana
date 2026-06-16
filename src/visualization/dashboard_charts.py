"""Plotly chart builders for the Streamlit dashboard.

This module contains pure chart-construction functions. Streamlit rendering
stays in app.py so the dashboard UI remains easy to understand.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def create_role_category_chart(df: pd.DataFrame) -> Figure:
    """Create role category distribution chart."""
    counts = (
        df["role_category"]
        .value_counts()
        .reset_index()
    )
    counts.columns = ["role_category", "offers"]

    return px.bar(
        counts,
        x="role_category",
        y="offers",
        text="offers",
        title="Distribución de ofertas por categoría de rol",
        labels={
            "role_category": "Categoría de rol",
            "offers": "Número de ofertas",
        },
    )


def create_work_mode_chart(df: pd.DataFrame) -> Figure:
    """Create work mode distribution chart."""
    counts = (
        df["work_mode"]
        .value_counts()
        .reset_index()
    )
    counts.columns = ["work_mode", "offers"]

    return px.pie(
        counts,
        names="work_mode",
        values="offers",
        title="Distribución por modalidad de trabajo",
    )


def create_role_by_work_mode_chart(df: pd.DataFrame) -> Figure:
    """Create relationship chart between role category and work mode."""
    return px.histogram(
        df,
        x="role_category",
        color="work_mode",
        barmode="group",
        title="Modalidad de trabajo por categoría de rol",
        labels={
            "role_category": "Categoría de rol",
            "work_mode": "Modalidad",
            "count": "Número de ofertas",
        },
    )


def create_seniority_chart(df: pd.DataFrame) -> Figure:
    """Create seniority distribution chart by role category."""
    return px.histogram(
        df,
        x="role_category",
        color="seniority",
        barmode="group",
        title="Seniority por categoría de rol",
        labels={
            "role_category": "Categoría de rol",
            "seniority": "Seniority",
            "count": "Número de ofertas",
        },
    )


def create_technologies_chart(df: pd.DataFrame) -> Figure | None:
    """Create most frequently detected technologies chart."""
    technologies = (
        df.assign(technology=df["technologies_detected"].str.split(", "))
        .explode("technology")
    )

    technologies["technology"] = technologies["technology"].fillna("").str.strip()
    technologies = technologies[technologies["technology"] != ""]

    if technologies.empty:
        return None

    counts = (
        technologies["technology"]
        .value_counts()
        .head(15)
        .reset_index()
    )
    counts.columns = ["technology", "mentions"]

    fig = px.bar(
        counts,
        x="mentions",
        y="technology",
        orientation="h",
        text="mentions",
        title="Tecnologías más mencionadas",
        labels={
            "technology": "Tecnología",
            "mentions": "Menciones",
        },
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    return fig


def create_timeline_chart(df: pd.DataFrame) -> Figure | None:
    """Create weekly evolution chart of job postings."""
    timeline = df.dropna(subset=["date_posted"]).copy()

    if timeline.empty:
        return None

    timeline["week"] = timeline["date_posted"].dt.to_period("W").dt.start_time

    counts = (
        timeline.groupby("week")
        .size()
        .reset_index(name="offers")
    )

    return px.line(
        counts,
        x="week",
        y="offers",
        markers=True,
        title="Evolución semanal de ofertas publicadas",
        labels={
            "week": "Semana",
            "offers": "Número de ofertas",
        },
    )


def create_salary_box_chart(salary_df: pd.DataFrame) -> Figure:
    """Create salary box plot for offers with explicitly published salary."""
    return px.box(
        salary_df,
        x="role_category",
        y="salary_offer_avg",
        points="all",
        title="Salario medio ofertado cuando está publicado",
        labels={
            "role_category": "Categoría de rol",
            "salary_offer_avg": "Salario medio ofertado",
        },
    )


def _simplify_ine_activity_branch(activity_branch: str) -> str:
    """Create a shorter label for INE activity branches."""
    if activity_branch == "Total":
        return "Total nacional"

    replacements = {
        "J Información y comunicaciones": "Información y comunicaciones",
        "K Actividades financieras y de seguros": "Finanzas y seguros",
        "M Actividades profesionales, científicas y técnicas": "Actividades profesionales",
        "D Suministro de energía eléctrica, gas, vapor y aire acondicionado": "Energía",
    }

    return replacements.get(activity_branch, activity_branch)


def create_ine_salary_context_chart(ine_df: pd.DataFrame) -> Figure | None:
    """Create INE sector-level salary context chart for the latest year."""
    context = ine_df[
        (ine_df["is_latest_year"] == True)
        & (ine_df["is_total_workday_type"] == True)
        & (ine_df["is_total_decile"] == True)
        & (ine_df["is_relevant_context_branch"] == True)
    ].copy()

    if context.empty:
        return None

    context["activity_branch_label"] = context["activity_branch"].apply(
        _simplify_ine_activity_branch
    )

    context = context.sort_values("salary_monthly_gross_eur", ascending=True)

    fig = px.bar(
        context,
        x="salary_monthly_gross_eur",
        y="activity_branch_label",
        orientation="h",
        text="salary_monthly_gross_eur",
        title="Contexto INE: salario mensual bruto por rama de actividad",
        labels={
            "salary_monthly_gross_eur": "Salario mensual bruto (€)",
            "activity_branch_label": "Rama de actividad",
        },
    )

    fig.update_traces(texttemplate="%{text:.0f} €", textposition="outside")

    return fig


def create_manfred_salary_reference_chart(manfred_df: pd.DataFrame) -> Figure | None:
    """Create Manfred tech salary reference chart for selected tech roles."""
    selected_roles = [
        "AI Engineer",
        "Backend",
        "Data Analyst",
        "Data Engineer",
        "Data Scientist",
        "Frontend",
        "Full-Stack",
        "MLOps",
        "QA & Testing",
        "SRE/DevOps",
        "Security/ Cybersecurity Engineer",
        "SysAdmin",
    ]

    selected_experience_ranges = [
        "<2 años",
        "2-5 años",
        "5-10 años",
    ]

    context = manfred_df[
        (manfred_df["salary_available"] == True)
        & (manfred_df["role_name"].isin(selected_roles))
        & (manfred_df["experience_range"].isin(selected_experience_ranges))
    ].copy()

    if context.empty:
        return None

    fig = px.bar(
        context,
        x="salary_midpoint_eur_year",
        y="role_name",
        color="experience_range",
        barmode="group",
        title="Referencia Manfred: salario anual por rol tech y experiencia",
        labels={
            "salary_midpoint_eur_year": "Salario anual de referencia (€)",
            "role_name": "Rol",
            "experience_range": "Experiencia",
        },
        category_orders={
            "experience_range": selected_experience_ranges,
        },
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    return fig
