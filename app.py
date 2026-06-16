from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.processing.dashboard_data import (
    apply_dashboard_filters,
    load_ine_salary_context_data,
    load_job_postings_data,
    load_manfred_salary_reference_data,
)
from src.visualization.dashboard_charts import (
    create_ine_salary_context_chart,
    create_manfred_salary_reference_chart,
    create_role_by_work_mode_chart,
    create_role_category_chart,
    create_salary_box_chart,
    create_seniority_chart,
    create_technologies_chart,
    create_timeline_chart,
    create_work_mode_chart,
)


DATA_PATH = Path("data/processed/job_postings_enriched.csv")
INE_SALARY_CONTEXT_PATH = Path("data/processed/ine_salary_context_processed.csv")
MANFRED_SALARY_REFERENCE_PATH = Path(
    "data/processed/manfred_salary_reference_processed.csv"
)


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


@st.cache_data
def load_ine_data(path: str) -> pd.DataFrame:
    """Load the processed INE salary context dataset."""
    return load_ine_salary_context_data(path)


@st.cache_data
def load_manfred_data(path: str) -> pd.DataFrame:
    """Load the processed Manfred salary reference dataset."""
    return load_manfred_salary_reference_data(path)


def render_custom_styles() -> None:
    """Render lightweight custom CSS for a more polished dashboard."""
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .hero-card {
                background: linear-gradient(135deg, #0F172A 0%, #1D4ED8 100%);
                padding: 2.2rem 2.4rem;
                border-radius: 1.25rem;
                color: white;
                margin-bottom: 1.5rem;
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.16);
            }

            .hero-eyebrow {
                text-transform: uppercase;
                letter-spacing: 0.12em;
                font-size: 0.78rem;
                font-weight: 700;
                opacity: 0.82;
                margin-bottom: 0.45rem;
            }

            .hero-title {
                font-size: 2.35rem;
                line-height: 1.12;
                font-weight: 800;
                margin-bottom: 0.75rem;
            }

            .hero-subtitle {
                font-size: 1.05rem;
                line-height: 1.55;
                max-width: 880px;
                opacity: 0.94;
                margin-bottom: 1.1rem;
            }

            .hero-tags {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
            }

            .hero-tag {
                background: rgba(255, 255, 255, 0.14);
                border: 1px solid rgba(255, 255, 255, 0.22);
                border-radius: 999px;
                padding: 0.32rem 0.75rem;
                font-size: 0.82rem;
                font-weight: 600;
            }

            .section-intro {
                margin-top: 0.8rem;
                margin-bottom: 0.9rem;
            }

            .section-intro h2 {
                margin-bottom: 0.2rem;
            }

            .section-intro p {
                color: #475569;
                margin-top: 0;
            }

            .kpi-card {
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 1rem;
                padding: 1rem 1.05rem;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
                min-height: 132px;
            }

            .kpi-label {
                color: #64748B;
                font-size: 0.78rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 0.45rem;
            }

            .kpi-value {
                color: #0F172A;
                font-size: 1.85rem;
                font-weight: 800;
                line-height: 1.1;
                margin-bottom: 0.35rem;
            }

            .kpi-help {
                color: #475569;
                font-size: 0.88rem;
                line-height: 1.35;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    """Render the main dashboard header."""
    st.markdown(
        """
        <section class="hero-card">
            <div class="hero-eyebrow">Proyecto II · Análisis y Visualización de Datos</div>
            <div class="hero-title">Radar del Mercado Tecnológico en España</div>
            <div class="hero-subtitle">
                Dashboard interactivo para explorar ofertas tecnológicas publicadas en España,
                identificar patrones por rol, modalidad, tecnologías y transparencia salarial,
                y comunicar conclusiones de forma clara.
            </div>
            <div class="hero-tags">
                <span class="hero-tag">Streamlit</span>
                <span class="hero-tag">Pandas</span>
                <span class="hero-tag">Plotly</span>
                <span class="hero-tag">Tecnoempleo + Ticjob</span>
                <span class="hero-tag">Contexto INE + Manfred</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
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

    flexible_work_rate = (
        (remote_or_hybrid / total_offers) * 100
        if total_offers > 0
        else 0
    )
    salary_transparency_rate = (
        (salary_available / total_offers) * 100
        if total_offers > 0
        else 0
    )

    st.markdown(
        """
        <div class="section-intro">
            <h2>Resumen ejecutivo</h2>
            <p>Indicadores principales de la muestra filtrada en el dashboard.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    kpis = [
        (
            col1,
            "Ofertas filtradas",
            f"{total_offers:,}".replace(",", "."),
            "Volumen de ofertas tras aplicar los filtros actuales.",
        ),
        (
            col2,
            "Empresas únicas",
            f"{total_companies:,}".replace(",", "."),
            "Número de compañías distintas presentes en la muestra.",
        ),
        (
            col3,
            "Remoto o híbrido",
            f"{remote_or_hybrid:,}".replace(",", "."),
            f"{flexible_work_rate:.1f}% de las ofertas filtradas.",
        ),
        (
            col4,
            "Salario publicado",
            f"{salary_available:,}".replace(",", "."),
            f"{salary_transparency_rate:.1f}% de transparencia salarial.",
        ),
    ]

    for column, label, value, help_text in kpis:
        column.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-help">{help_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


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


def render_external_salary_context_section(
    ine_df: pd.DataFrame,
    manfred_df: pd.DataFrame,
) -> None:
    """Render external salary context from INE and Manfred."""
    st.subheader("Contexto salarial externo")

    if ine_df.empty and manfred_df.empty:
        st.info(
            """
            No se han encontrado los datasets externos de contexto salarial.
            Esta sección se puede regenerar con los scripts de procesamiento correspondientes.
            """
        )
        return

    st.info(
        """
        Esta sección añade contexto externo para interpretar mejor la transparencia salarial
        observada en las ofertas.

        **INE** aporta contexto oficial por rama de actividad, pero no representa salarios
        tecnológicos por rol.

        **Manfred** aporta una referencia salarial tecnológica por rol y experiencia,
        pero no representa salarios observados en las ofertas analizadas.

        Estos datos no se usan para rellenar salarios ausentes ni para sustituir los salarios
        publicados explícitamente en las ofertas.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Contexto sectorial oficial — INE")
        st.caption(
            "Salario mensual bruto por rama de actividad. Fuente oficial sectorial, no específica por rol tech."
        )

        ine_fig = create_ine_salary_context_chart(ine_df)

        if ine_fig is None:
            st.info("No hay datos de INE suficientes para mostrar este gráfico.")
        else:
            st.plotly_chart(ine_fig, width="stretch")

    with col2:
        st.markdown("#### Referencia tecnológica — Manfred")
        st.caption(
            "Rangos salariales tecnológicos por rol y experiencia. Referencia externa, no observación de ofertas."
        )

        manfred_fig = create_manfred_salary_reference_chart(manfred_df)

        if manfred_fig is None:
            st.info("No hay datos de Manfred suficientes para mostrar este gráfico.")
        else:
            st.plotly_chart(manfred_fig, width="stretch")


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
    render_custom_styles()
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

    ine_df = (
        load_ine_data(str(INE_SALARY_CONTEXT_PATH))
        if INE_SALARY_CONTEXT_PATH.exists()
        else pd.DataFrame()
    )
    manfred_df = (
        load_manfred_data(str(MANFRED_SALARY_REFERENCE_PATH))
        if MANFRED_SALARY_REFERENCE_PATH.exists()
        else pd.DataFrame()
    )

    render_external_salary_context_section(ine_df, manfred_df)

    st.divider()

    render_storytelling_notes(filtered)
    render_data_table(filtered)


if __name__ == "__main__":
    main()
