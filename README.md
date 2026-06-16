# Radar del mercado tech en España

Dashboard interactivo desarrollado con **Streamlit**, **Pandas** y **Plotly** para explorar ofertas de empleo tecnológico en España durante 2026.

El proyecto está orientado a un público no técnico y busca responder preguntas de negocio como:

- qué perfiles tecnológicos concentran más demanda;
- qué modalidades de trabajo aparecen con más frecuencia;
- qué tecnologías se mencionan más en las ofertas;
- qué nivel de experiencia se solicita;
- cuánta transparencia salarial existe en las ofertas;
- qué sesgos y limitaciones deben tenerse en cuenta antes de tomar decisiones.

## Estado del proyecto

Proyecto en desarrollo para el **Proyecto II del Módulo II** del bootcamp.

Estado actual:

- Dashboard funcional en Streamlit.
- Dataset principal procesado localmente.
- Filtros interactivos.
- Más de 4 visualizaciones conectadas.
- Storytelling ejecutivo y advertencias metodológicas.
- Contexto salarial externo mediante INE y Manfred.
- Código modularizado en `src/`.
- README inicial de entrega documentado.

Pendiente:

- Despliegue público en la nube.
- URL pública del dashboard.
- Validación con usuario real no técnico.
- Documentación metodológica final en `docs/data_strategy.md`.

## Demo

URL pública del dashboard:

```text
Pendiente de despliegue.
```

Ejecución local:

```bash
streamlit run app.py
```

## Estructura del proyecto

```text
.
├── app.py
├── data
│   ├── raw
│   ├── interim
│   └── processed
├── docs
│   └── data_strategy.md
├── README.md
├── requirements.txt
├── src
│   ├── extraction
│   ├── features
│   ├── processing
│   └── visualization
└── .streamlit
    └── config.toml
```

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

La carpeta `data/` mantiene solo su estructura mediante archivos `.gitkeep`. Los datos se generan localmente mediante scripts reproducibles.

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

## Validación con usuario no técnico

Pendiente.

La validación final deberá comprobar que una persona externa al desarrollo puede:

* entender los KPIs principales;
* usar los filtros;
* interpretar al menos 2 o 3 gráficos;
* comprender las limitaciones y sesgos;
* explicar con sus palabras una conclusión del dashboard.

## Próximos pasos

* Actualizar `docs/data_strategy.md` con la metodología final.
* Subir el repositorio a GitHub.
* Preparar despliegue público.
* Añadir URL pública al README.
* Realizar validación con usuario no técnico.
* Preparar presentación ejecutiva de 7 minutos.

## Autor

David Rojas Cruz

Proyecto desarrollado como parte del bootcamp de Inteligencia Artificial.
