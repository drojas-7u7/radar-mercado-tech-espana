"""Plotly chart builders for the Streamlit dashboard.

This module contains pure chart-construction functions. Streamlit rendering
stays in app.py so the dashboard UI remains easy to understand.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


SOFT_COLOR_SEQUENCE = [
    "#6B8FB3",  # soft blue
    "#8FB996",  # soft green
    "#D9A66A",  # soft amber
    "#B7A6C9",  # soft purple
    "#A8B0B8",  # soft neutral gray
    "#D98C8C",  # soft coral
    "#7895A8",  # blue gray
]

WORK_MODE_COLOR_MAP = {
    "remote": "#8FB996",
    "hybrid": "#6B8FB3",
    "onsite": "#D9A66A",
    "unknown": "#A8B0B8",
}

SENIORITY_COLOR_MAP = {
    "junior": "#8FB996",
    "mid": "#6B8FB3",
    "senior": "#B7A6C9",
    "lead": "#D9A66A",
    "unknown": "#A8B0B8",
}

EXPERIENCE_RANGE_COLOR_MAP = {
    "<2 años": "#8FB996",
    "2-5 años": "#6B8FB3",
    "5-10 años": "#B7A6C9",
}

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = SOFT_COLOR_SEQUENCE


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
        title="¿Qué perfiles concentran más demanda?",
        labels={
            "role_category": "Perfil profesional",
            "offers": "Ofertas",
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
        color="work_mode",
        color_discrete_map=WORK_MODE_COLOR_MAP,
        title="¿Qué modalidad de trabajo ofrece el mercado?",
    )


def create_role_by_work_mode_chart(df: pd.DataFrame) -> Figure:
    """Create relationship chart between role category and work mode."""
    return px.histogram(
        df,
        x="role_category",
        color="work_mode",
        color_discrete_map=WORK_MODE_COLOR_MAP,
        barmode="group",
        title="¿Dónde hay más opciones de remoto, híbrido o presencial?",
        labels={
            "role_category": "Perfil profesional",
            "work_mode": "Modalidad de trabajo",
            "count": "Ofertas",
        },
    )


def create_seniority_chart(df: pd.DataFrame) -> Figure:
    """Create seniority distribution chart by role category."""
    return px.histogram(
        df,
        x="role_category",
        color="seniority",
        color_discrete_map=SENIORITY_COLOR_MAP,
        barmode="group",
        title="¿Qué nivel de experiencia se pide en cada perfil?",
        labels={
            "role_category": "Perfil profesional",
            "seniority": "Nivel de experiencia",
            "count": "Ofertas",
        },
        category_orders={
            "seniority": ["junior", "mid", "senior", "lead", "unknown"],
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
        title="¿Qué tecnologías aparecen con más frecuencia?",
        labels={
            "technology": "Tecnología",
            "mentions": "Apariciones en ofertas",
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
        title="¿Cómo evoluciona la publicación de ofertas en 2026?",
        labels={
            "week": "Semana",
            "offers": "Ofertas",
        },
    )



def create_description_length_distribution_chart(df: pd.DataFrame) -> Figure | None:
    """Create distribution chart for job posting description length."""
    if "description_length" not in df.columns:
        return None

    distribution = df.copy()
    distribution["description_length"] = pd.to_numeric(
        distribution["description_length"],
        errors="coerce",
    )
    distribution = distribution.dropna(subset=["description_length"])
    distribution = distribution[distribution["description_length"] > 0]

    if distribution.empty:
        return None

    fig = px.histogram(
        distribution,
        x="description_length",
        nbins=30,
        title="¿Cómo se distribuye el nivel de detalle de las ofertas?",
        labels={
            "description_length": "Longitud de la descripción de la oferta",
            "count": "Número de ofertas",
        },
    )

    fig.update_layout(
        xaxis_title="Longitud de la descripción de la oferta",
        yaxis_title="Número de ofertas",
    )

    return fig


def create_salary_box_chart(salary_df: pd.DataFrame) -> Figure:
    """Create salary box plot for offers with explicitly published salary."""
    return px.box(
        salary_df,
        x="role_category",
        y="salary_offer_avg",
        points="all",
        title="¿Qué salarios se publican cuando la oferta los muestra?",
        labels={
            "role_category": "Perfil profesional",
            "salary_offer_avg": "Salario medio publicado (€)",
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
        title="Contexto oficial: comparación salarial por sector",
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
        color_discrete_map=EXPERIENCE_RANGE_COLOR_MAP,
        barmode="group",
        title="Referencia tecnológica: salario anual orientativo por rol y experiencia",
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
