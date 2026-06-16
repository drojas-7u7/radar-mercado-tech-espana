<div align="center">

# Radar del mercado tech en España

<br>

<span style="font-size: 1.2em;">
Dashboard interactivo para analizar ofertas tecnológicas publicadas en España durante 2026
</span>

<br><br>

[Ver dashboard desplegado](https://radar-mercado-tech-espana-t6vqbotubuzgoswrbxhlt9.streamlit.app/) ·
[Ver repositorio en GitHub](https://github.com/drojas-7u7/radar-mercado-tech-espana) ·
[Ver estrategia de datos](docs/data_strategy.md)

</div>

---

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Análisis%20de%20datos-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Gráficos%20interactivos-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-Repositorio-181717?style=for-the-badge&logo=github&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-Desplegado-success?style=for-the-badge)

---

## Contenidos

| Sección | Enlace |
|---------|--------|
| Resumen del proyecto | [Ir a sección](#resumen-del-proyecto) |
| Estado del proyecto | [Ir a sección](#estado-del-proyecto) |
| Demo | [Ir a sección](#demo) |
| Estructura del proyecto | [Ir a sección](#estructura-del-proyecto) |
| Herramientas utilizadas | [Ir a sección](#herramientas-utilizadas) |
| Justificación de la herramienta | [Ir a sección](#justificación-de-la-herramienta) |
| Fuentes de datos | [Ir a sección](#fuentes-de-datos) |
| Importante sobre los datos | [Ir a sección](#importante-sobre-los-datos) |
| Flujo de generación de datos | [Ir a sección](#flujo-de-generación-de-datos) |
| Visualizaciones del dashboard | [Ir a sección](#visualizaciones-del-dashboard) |
| Filtros disponibles | [Ir a sección](#filtros-disponibles) |
| Lectura de negocio | [Ir a sección](#lectura-de-negocio) |
| Limitaciones y sesgos | [Ir a sección](#limitaciones-y-sesgos) |
| Riesgo de uso incorrecto | [Ir a sección](#riesgo-de-uso-incorrecto) |
| Recomendaciones operativas | [Ir a sección](#recomendaciones-operativas) |
| Instalación local | [Ir a sección](#instalación-local) |
| Requisitos | [Ir a sección](#requisitos) |
| Autor | [Ir a sección](#autor) |

---

## Resumen del proyecto

**Radar del mercado tech en España** es un dashboard interactivo desarrollado con **Python**, **Streamlit**, **Pandas** y **Plotly** para explorar una muestra de ofertas tecnológicas publicadas en España durante 2026.

El proyecto está orientado a una audiencia no técnica y busca transformar datos de ofertas laborales en una lectura visual, clara y defendible sobre el mercado tecnológico español.

El dashboard permite responder preguntas como:

* Qué perfiles tecnológicos concentran más demanda.
* Qué modalidades de trabajo aparecen con más frecuencia.
* Qué tecnologías se mencionan más en las ofertas.
* Qué nivel de experiencia se solicita.
* Cuánta transparencia salarial existe en las ofertas.
* Qué sesgos y limitaciones deben tenerse en cuenta antes de tomar decisiones.

---

## Estado del proyecto

Proyecto desarrollado para el **Proyecto II del Módulo II** del bootcamp.

Estado actual:

* Dashboard funcional en Streamlit.
* Dashboard desplegado públicamente en Streamlit Cloud.
* Dataset principal procesado y filtrado a ofertas de 2026.
* Filtros interactivos.
* Más de 4 visualizaciones conectadas.
* Storytelling ejecutivo y advertencias metodológicas.
* Contexto salarial externo mediante INE y Manfred.
* Código modularizado en `src/`.
* Documentación metodológica en `docs/data_strategy.md`.

---

## Demo

Dashboard desplegado:

```text
https://radar-mercado-tech-espana-t6vqbotubuzgoswrbxhlt9.streamlit.app/
```

Ejecución local:

```bash
streamlit run app.py
```

---

## Estructura del proyecto

A nivel de directorios, el proyecto se organiza de la siguiente manera:

```text
radar-mercado-tech-espana/
│
├── 📄 README.md                              ← Documentación principal del proyecto
├── 📄 requirements.txt                       ← Dependencias necesarias para ejecutar la aplicación
├── 📄 .gitignore                             ← Reglas de exclusión para Git
├── 🚀 app.py                                 ← Aplicación principal de Streamlit
│
├── ⚙️ .streamlit/                            ← Configuración de Streamlit
│   └── config.toml                           ← Configuración visual de la aplicación
│
├── 📁 data/                                  ← Datos del proyecto
│   ├── raw/                                  ← URLs candidatas y datos originales
│   │   ├── tecnoempleo_candidate_urls.csv
│   │   └── ticjob_candidate_urls.csv
│   │
│   ├── interim/                              ← Datos intermedios del proceso de extracción
│   │   ├── job_urls.csv
│   │   ├── job_postings_normalized.csv
│   │   ├── job_postings_extraction_errors.csv
│   │   └── full_job_posting_extraction.log
│   │
│   └── processed/                            ← Datos finales usados por el dashboard
│       ├── job_postings_enriched.csv
│       ├── ine_salary_context_processed.csv
│       └── manfred_salary_reference_processed.csv
│
├── 📁 docs/                                  ← Documentación metodológica
│   └── data_strategy.md                      ← Estrategia de datos, fuentes, sesgos y trazabilidad
│
└── 📁 src/                                   ← Código fuente modularizado
    │
    ├── 📁 extraction/                        ← Extracción de URLs y ofertas laborales
    │   ├── check_sources.py
    │   ├── collect_candidate_job_urls.py
    │   ├── extract_job_postings_from_urls.py
    │   └── job_posting_extractor.py
    │
    ├── 📁 features/                          ← Enriquecimiento y clasificación del dataset
    │   └── enrich_job_postings.py
    │
    ├── 📁 processing/                        ← Preparación, carga y contexto de datos
    │   ├── dashboard_data.py
    │   ├── prepare_ine_salary_context.py
    │   └── prepare_manfred_salary_reference.py
    │
    └── 📁 visualization/                     ← Construcción de gráficos interactivos
        └── dashboard_charts.py
```

---

## Herramientas utilizadas

* **Python**: lenguaje principal del proyecto.
* **Pandas**: carga, limpieza, transformación y análisis de datos.
* **Plotly**: creación de visualizaciones interactivas.
* **Streamlit**: construcción y despliegue del dashboard.
* **BeautifulSoup / requests / lxml / html5lib**: extracción y procesamiento de fuentes web.
* **Git**: control de versiones.

## Justificación de la herramienta

Se utiliza **Streamlit** porque permite construir dashboards interactivos en Python de forma rápida, clara y reproducible. Es una herramienta adecuada para este proyecto porque:

* permite desarrollar una aplicación web sin separar frontend y backend;
* se integra bien con Pandas y Plotly;
* facilita filtros interactivos para usuarios no técnicos;
* permite desplegar el dashboard en la nube;
* mantiene el proyecto dentro del ecosistema Python trabajado durante el bootcamp.

## Fuentes de datos

### 1. Dataset principal de ofertas tech

El dataset principal se construye a partir de ofertas tecnológicas publicadas en:

* **Tecnoempleo**
* **Ticjob**

El proceso genera un dataset procesado en:

```text
data/processed/job_postings_enriched.csv
```

Resumen del dataset principal local:

| Métrica                        |                   Valor |
| ------------------------------ | ----------------------: |
| Filas                          |                   2.240 |
| Columnas                       |                      23 |
| Rango temporal                 | 2026-01-02 a 2026-06-15 |
| Ofertas de Tecnoempleo         |                   2.128 |
| Ofertas de Ticjob              |                     112 |
| Ofertas con salario publicado  |                      28 |
| Ofertas sin salario disponible |                   2.212 |

Columnas principales:

* `source`
* `url`
* `title`
* `company`
* `date_posted`
* `salary_offer_min`
* `salary_offer_max`
* `salary_offer_avg`
* `salary_data_type`
* `description_length`
* `location_locality`
* `location_region`
* `work_mode`
* `seniority`
* `technologies_detected`
* `role_category`

### 2. Contexto salarial oficial INE

Fuente:

```text
INE - Salarios medios por tipo de jornada, rama de actividad y decil. EPA
https://www.ine.es/jaxiT3/files/t/csv_bd/66245.csv
```

Archivo procesado local:

```text
data/processed/ine_salary_context_processed.csv
```

Resumen local:

| Métrica  |  Valor |
| -------- | -----: |
| Filas    | 12.342 |
| Columnas |     17 |

Uso en el proyecto:

* Se usa como contexto oficial sectorial.
* No representa salarios específicos de roles tecnológicos.
* No se usa para rellenar salarios ausentes en ofertas.
* No sustituye al dataset principal de ofertas.

### 3. Referencia salarial tecnológica Manfred

Fuente:

```text
Manfred - Guía Salarial 2026 - Salarios en tecnología [España]
https://www.getmanfred.com/blog/guia-salarial-2026-salarios-en-tecnologia-espana-manfred/
```

Archivo procesado local:

```text
data/processed/manfred_salary_reference_processed.csv
```

Resumen local:

| Métrica  | Valor |
| -------- | ----: |
| Filas    |    80 |
| Columnas |    19 |

Uso en el proyecto:

* Se usa como referencia salarial tecnológica por rol y experiencia.
* No representa salarios observados directamente en las ofertas analizadas.
* No se usa para imputar salarios ausentes.
* Sirve como contexto complementario para interpretar la transparencia salarial de las ofertas.

## Importante sobre los datos

Los CSV generados no están versionados en Git por defecto.

Como excepción práctica para el despliegue del dashboard, el repositorio incluye únicamente los CSV procesados finales necesarios para ejecutar la aplicación:

- `data/processed/job_postings_enriched.csv`
- `data/processed/ine_salary_context_processed.csv`
- `data/processed/manfred_salary_reference_processed.csv`

El resto de datos raw, intermedios o generados durante el proceso siguen excluidos de Git mediante `.gitignore`.

La carpeta `data/` mantiene su estructura mediante archivos `.gitkeep`, y los datos pueden regenerarse localmente mediante los scripts reproducibles incluidos en el repositorio.

Esto se hace para evitar subir al repositorio archivos generados, intermedios o potencialmente pesados, y para mantener una separación clara entre:

* código fuente;
* datos raw;
* datos intermedios;
* datos procesados;
* documentación metodológica.

Para ejecutar el dashboard localmente, deben existir estos archivos:

```text
data/processed/job_postings_enriched.csv
data/processed/ine_salary_context_processed.csv
data/processed/manfred_salary_reference_processed.csv
```

El archivo obligatorio para que el dashboard arranque es:

```text
data/processed/job_postings_enriched.csv
```

Los datasets de INE y Manfred son complementarios. Si no existen, el dashboard principal puede seguir funcionando, pero se pierde el contexto salarial externo.

## Flujo de generación de datos

### 1. Comprobar fuentes

```bash
python src/extraction/check_sources.py
```

### 2. Recoger URLs candidatas desde los sitemaps

```bash
python src/extraction/collect_candidate_job_urls.py
```

Genera:

```text
data/raw/tecnoempleo_candidate_urls.csv
data/raw/ticjob_candidate_urls.csv
data/interim/job_urls.csv
```

### 3. Extraer y normalizar ofertas

```bash
python src/extraction/extract_job_postings_from_urls.py
```

Genera:

```text
data/interim/job_postings_normalized.csv
data/interim/job_postings_extraction_errors.csv
```

Este paso puede tardar bastante tiempo porque recorre múltiples URLs de ofertas.

### 4. Enriquecer el dataset principal

```bash
python src/features/enrich_job_postings.py
```

Genera:

```text
data/processed/job_postings_enriched.csv
```

El enriquecimiento añade campos como:

* modalidad de trabajo estimada;
* seniority estimado;
* tecnologías detectadas;
* categoría profesional aproximada;
* normalización de país;
* tipo de dato salarial.

### 5. Preparar contexto salarial INE

```bash
python src/processing/prepare_ine_salary_context.py
```

Genera:

```text
data/processed/ine_salary_context_processed.csv
```

### 6. Preparar referencia salarial Manfred

```bash
python src/processing/prepare_manfred_salary_reference.py
```

Genera:

```text
data/processed/manfred_salary_reference_processed.csv
```

### 7. Ejecutar el dashboard

```bash
streamlit run app.py
```

## Visualizaciones del dashboard

El dashboard incluye:

* KPIs principales de la muestra filtrada.
* Distribución de ofertas por perfil profesional.
* Distribución por modalidad de trabajo.
* Cruce entre perfil profesional y modalidad.
* Nivel de experiencia solicitado por perfil.
* Tecnologías más mencionadas.
* Evolución temporal de publicación de ofertas.
* Distribución estadística del nivel de detalle de las ofertas.
* Transparencia salarial en ofertas con salario publicado.
* Comparativa de contexto salarial oficial INE.
* Referencia salarial tecnológica Manfred.
* Tabla exploratoria filtrable.

## Filtros disponibles

El dashboard permite segmentar la muestra por:

* fuente;
* perfil profesional;
* modalidad de trabajo;
* nivel de experiencia;
* región;
* rango de fechas;
* tecnología detectada.

Los filtros afectan de forma conjunta a los KPIs, gráficos y tabla de datos.

## Lectura de negocio

El dashboard permite explorar el mercado tecnológico español desde una perspectiva práctica:

* identificar perfiles con mayor volumen de ofertas;
* detectar peso relativo del trabajo remoto, híbrido y presencial;
* observar qué tecnologías se repiten con más frecuencia;
* analizar si las ofertas explican con suficiente detalle sus requisitos;
* medir la transparencia salarial real de las ofertas;
* comparar la muestra con referencias salariales externas sin mezclar fuentes incompatibles.

## Limitaciones y sesgos

Este proyecto debe interpretarse como un análisis exploratorio, no como una medición completa del mercado laboral tecnológico español.

Principales limitaciones:

* La muestra procede de portales concretos, por lo que existe sesgo de fuente.
* El dataset no representa todas las ofertas tecnológicas publicadas en España.
* Tecnoempleo tiene mucho más peso que Ticjob en la muestra.
* Las categorías de perfil se asignan mediante reglas, por lo que pueden existir clasificaciones imperfectas.
* La modalidad de trabajo y el seniority no siempre aparecen explícitos.
* La disponibilidad salarial es muy baja: solo 28 de 2.240 ofertas tienen salario publicado.
* Los salarios publicados no deben interpretarse como salario medio real del mercado.
* INE y Manfred son fuentes de contexto, no sustitutos del dataset principal.

## Riesgo de uso incorrecto

Usar este dashboard sin tener en cuenta los sesgos podría llevar a decisiones equivocadas, por ejemplo:

* asumir que la categoría con más ofertas en la muestra representa todo el mercado;
* interpretar la falta de salario como salario bajo o inexistente;
* tomar decisiones salariales usando solo las 28 ofertas con salario publicado;
* mezclar salarios sectoriales del INE con salarios por rol tecnológico;
* usar la referencia Manfred como si fueran salarios observados en las ofertas;
* considerar como exactas categorías que son aproximaciones basadas en reglas.

## Recomendaciones operativas

* Usar el dashboard como herramienta exploratoria y de orientación.
* Complementar el análisis con más fuentes antes de tomar decisiones económicas relevantes.
* Tratar los salarios publicados como indicador de transparencia salarial, no como salario medio.
* Priorizar la interpretación por perfiles, modalidad y tecnologías.
* Documentar siempre la fuente y el método antes de reutilizar los datos.

## Instalación local

Crear y activar un entorno virtual o Conda.

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
streamlit run app.py
```

## Requisitos

Dependencias principales:

```text
pandas
numpy
streamlit
plotly
requests
beautifulsoup4
lxml
html5lib
scipy
python-dotenv
```

Las versiones concretas están fijadas en `requirements.txt`.

## Autor

David Rojas Cruz

Proyecto desarrollado como parte del bootcamp de Inteligencia Artificial.
