from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.processing.dashboard_data import apply_dashboard_filters, load_job_postings_data
from src.visualization.dashboard_charts import (
    create_role_by_work_mode_chart,
    create_role_category_chart,
    create_salary_box_chart,
    create_seniority_chart,
    create_technologies_chart,
    create_timeline_chart,
    create_work_mode_chart,
)


DATA_PATH = Path("data/processed/job_postings_enriched.csv")


def configure_page() -> None:
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Radar del Mercado Tech en España",
        layout="wide",
    )


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load the processed job postings dataset."""
    return load_job_postings_data(path)


def render_header() -> None:
    """Render the main dashboard header."""
    st.title("Radar del Mercado Tecnológico en España")
    st.subheader("Dashboard interactivo sobre ofertas, perfiles y tecnologías del sector tech")

    st.markdown(
        """
        Esta aplicación forma parte del Proyecto II del Módulo II: Análisis y Visualización de Datos.

        El objetivo es transformar ofertas reales del mercado laboral tecnológico en España en conclusiones
        claras para una audiencia no técnica.
        """
    )


def render_sidebar_filters(df: pd.DataFrame) -> dict:
    """Render sidebar filters and return selected values."""
    st.sidebar.header("Filtros")

    sources = sorted(df["source"].dropna().unique())
    role_categories = sorted(df["role_category"].dropna().unique())
    work_modes = sorted(df["work_mode"].dropna().unique())
    seniorities = sorted(df["seniority"].dropna().unique())

    selected_sources = st.sidebar.multiselect(
        "Fuente",
        options=sources,
        default=sources,
    )

    selected_roles = st.sidebar.multiselect(
        "Categoría de rol",
        options=role_categories,
        default=role_categories,
    )

    selected_work_modes = st.sidebar.multiselect(
        "Modalidad de trabajo",
        options=work_modes,
        default=work_modes,
    )

    selected_seniorities = st.sidebar.multiselect(
        "Seniority",
        options=seniorities,
        default=seniorities,
    )

    min_date = df["date_posted"].min().date()
    max_date = df["date_posted"].max().date()

    selected_date_range = st.sidebar.date_input(
        "Rango de fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    return {
        "sources": selected_sources,
        "roles": selected_roles,
        "work_modes": selected_work_modes,
        "seniorities": selected_seniorities,
        "date_range": selected_date_range,
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply sidebar filters to the dataset."""
    return apply_dashboard_filters(df, filters)


def render_kpis(df: pd.DataFrame) -> None:
    """Render top-level KPI cards."""
    total_offers = len(df)
    total_companies = df["company"].nunique()
    remote_or_hybrid = df[df["work_mode"].isin(["remote", "hybrid"])].shape[0]
    salary_available = df[df["salary_data_type"] == "published_in_offer"].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Ofertas analizadas", f"{total_offers}")
    col2.metric("Empresas únicas", f"{total_companies}")
    col3.metric("Remoto o híbrido", f"{remote_or_hybrid}")
    col4.metric("Con salario publicado", f"{salary_available}")


def render_role_category_chart(df: pd.DataFrame) -> None:
    """Render role category distribution chart."""
    fig = create_role_category_chart(df)
    st.plotly_chart(fig, width="stretch")


def render_work_mode_chart(df: pd.DataFrame) -> None:
    """Render work mode distribution chart."""
    fig = create_work_mode_chart(df)
    st.plotly_chart(fig, width="stretch")


def render_role_by_work_mode_chart(df: pd.DataFrame) -> None:
    """Render relationship between role category and work mode."""
    fig = create_role_by_work_mode_chart(df)
    st.plotly_chart(fig, width="stretch")


def render_seniority_chart(df: pd.DataFrame) -> None:
    """Render seniority distribution by role category."""
    fig = create_seniority_chart(df)
    st.plotly_chart(fig, width="stretch")


def render_technologies_chart(df: pd.DataFrame) -> None:
    """Render most frequently detected technologies."""
    fig = create_technologies_chart(df)

    if fig is None:
        st.info("No hay tecnologías detectadas con los filtros actuales.")
        return

    st.plotly_chart(fig, width="stretch")


def render_timeline_chart(df: pd.DataFrame) -> None:
    """Render weekly evolution of job postings."""
    fig = create_timeline_chart(df)

    if fig is None:
        st.info("No hay fechas válidas con los filtros actuales.")
        return

    st.plotly_chart(fig, width="stretch")


def render_salary_section(df: pd.DataFrame) -> None:
    """Render salary transparency analysis with limitations."""
    st.subheader("Transparencia salarial")

    total_offers = len(df)

    salary_df = df[
        (df["salary_data_type"] == "published_in_offer")
        & (df["salary_offer_avg"].notna())
    ].copy()

    salary_available = len(salary_df)
    salary_missing = max(total_offers - salary_available, 0)
    transparency_rate = (
        (salary_available / total_offers) * 100
        if total_offers > 0
        else 0
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Ofertas filtradas", f"{total_offers}")
    col2.metric("Con salario publicado", f"{salary_available}")
    col3.metric("Transparencia salarial", f"{transparency_rate:.1f}%")

    st.info(
        f"""
        En la muestra filtrada, **{salary_available} de {total_offers} ofertas**
        publican un salario utilizable. Las otras **{salary_missing} ofertas**
        no permiten calcular un salario medio ofertado.

        Por eso, esta sección mide principalmente la **transparencia salarial**
        de las ofertas, no el salario real del mercado tecnológico.
        """
    )

    if salary_df.empty:
        st.warning("No hay salarios publicados con los filtros actuales.")
        return

    st.warning(
        """
        El gráfico siguiente solo usa ofertas con salario publicado explícitamente.
        Debe leerse como una muestra parcial, no como una estimación salarial representativa del mercado.
        """
    )

    fig = create_salary_box_chart(salary_df)

    st.plotly_chart(fig, width="stretch")


def render_storytelling_notes(df: pd.DataFrame) -> None:
    """Render key interpretation notes for non-technical users."""
    st.subheader("Lectura inicial")

    top_role = df["role_category"].value_counts().idxmax()
    top_work_mode = df["work_mode"].value_counts().idxmax()
    salary_missing = df["salary_offer_avg"].isna().sum()
    total_rows = len(df)

    st.markdown(
        f"""
        En la muestra filtrada, la categoría con más ofertas es **{top_role}** y la modalidad más frecuente
        es **{top_work_mode}**.

        El análisis salarial debe interpretarse con cautela: **{salary_missing} de {total_rows} ofertas**
        no tienen salario medio disponible.

        Esta clasificación de roles y tecnologías se basa en reglas transparentes aplicadas sobre los textos
        de las ofertas. Por tanto, puede contener errores puntuales, pero permite construir una primera visión
        exploratoria del mercado.
        """
    )


def render_data_table(df: pd.DataFrame) -> None:
    """Render filtered data table."""
    with st.expander("Ver datos filtrados"):
        columns = [
            "source",
            "title",
            "company",
            "date_posted",
            "role_category",
            "work_mode",
            "seniority",
            "technologies_detected",
            "salary_offer_avg",
            "salary_data_type",
            "url",
        ]

        st.dataframe(df[columns], width="stretch")


def main() -> None:
    """Run the Streamlit app."""
    configure_page()
    render_header()

    if not DATA_PATH.exists():
        st.error(f"No se ha encontrado el dataset procesado: {DATA_PATH}")
        st.stop()

    df = load_data(str(DATA_PATH))

    filters = render_sidebar_filters(df)
    filtered = apply_filters(df, filters)

    if filtered.empty:
        st.warning("No hay ofertas que coincidan con los filtros seleccionados.")
        st.stop()

    render_kpis(filtered)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        render_role_category_chart(filtered)

    with col2:
        render_work_mode_chart(filtered)

    col3, col4 = st.columns(2)

    with col3:
        render_role_by_work_mode_chart(filtered)

    with col4:
        render_seniority_chart(filtered)

    render_technologies_chart(filtered)
    render_timeline_chart(filtered)
    render_salary_section(filtered)

    st.divider()

    render_storytelling_notes(filtered)
    render_data_table(filtered)


if __name__ == "__main__":
    main()
