import streamlit as st


def configure_page() -> None:
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Radar del Mercado Tech en España",
        layout="wide",
    )


def render_header() -> None:
    """Render the main dashboard header."""
    st.title("Radar del Mercado Tecnológico en España")
    st.subheader("Dashboard interactivo sobre ofertas, perfiles, tecnologías y salarios del sector tech")

    st.markdown(
        """
        Esta aplicación forma parte del Proyecto II del Módulo II: Análisis y Visualización de Datos.

        El objetivo es transformar datos del mercado laboral tecnológico en España en conclusiones claras
        para una audiencia no técnica.
        """
    )


def main() -> None:
    """Run the Streamlit app."""
    configure_page()
    render_header()

    st.info("Versión inicial del dashboard. Próximo paso: validar fuentes de datos y construir el dataset.")


if __name__ == "__main__":
    main()
