# Estrategia de datos

## 1. Objetivo del documento

Este documento describe la estrategia de datos seguida en el proyecto `radar-mercado-tech-espana`.

El objetivo es dejar documentado:

- qué fuentes de datos se usan;
- cómo se generan los datasets locales;
- qué transformaciones se aplican;
- qué variables se utilizan en el dashboard;
- qué limitaciones y sesgos existen;
- qué decisiones metodológicas se han tomado para evitar interpretaciones incorrectas.

El proyecto se centra en construir un dashboard interactivo y narrativo para público no técnico, por lo que la estrategia de datos prioriza trazabilidad, claridad, reproducibilidad y honestidad metodológica.

---

## 2. Resumen de la estrategia

La estrategia de datos se basa en combinar:

1. Un dataset principal de ofertas tecnológicas en España.
2. Una fuente oficial de contexto salarial sectorial.
3. Una referencia salarial tecnológica externa por rol y experiencia.

El dataset principal permite analizar la muestra real de ofertas recopiladas.

Las fuentes complementarias ayudan a contextualizar la lectura salarial, pero no sustituyen al dataset principal ni se usan para rellenar valores ausentes.

---

## 3. Fuentes utilizadas

### 3.1 Dataset principal de ofertas tech

El dataset principal se construye a partir de ofertas tecnológicas publicadas en:

- Tecnoempleo.
- Ticjob.

Estas fuentes se usan porque están especializadas o muy orientadas al empleo tecnológico en España.

El archivo procesado final es:

```text
data/processed/job_postings_enriched.csv
```

Resumen local del dataset procesado:

| Métrica | Valor |
| --- | ---: |
| Filas | 2.240 |
| Columnas | 23 |
| Rango temporal | 2026-01-02 a 2026-06-15 |
| Ofertas de Tecnoempleo | 2.128 |
| Ofertas de Ticjob | 112 |
| Ofertas con salario publicado | 28 |
| Ofertas sin salario disponible | 2.212 |

Este dataset es la base principal del dashboard.

---

### 3.2 Fuente complementaria INE

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

| Métrica | Valor |
| --- | ---: |
| Filas | 12.342 |
| Columnas | 17 |

Uso metodológico:

- Se usa como contexto oficial sectorial.
- Permite comparar sectores amplios como información y comunicaciones, actividades financieras, energía o total nacional.
- No representa salarios específicos de roles tecnológicos.
- No se usa para imputar salarios ausentes.
- No sustituye al dataset principal.

---

### 3.3 Fuente complementaria Manfred

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

| Métrica | Valor |
| --- | ---: |
| Filas | 80 |
| Columnas | 19 |

Uso metodológico:

- Se usa como referencia salarial tecnológica por rol y rango de experiencia.
- No representa salarios observados directamente en las ofertas analizadas.
- No se usa para imputar salarios ausentes.
- Sirve como contexto complementario para interpretar la baja transparencia salarial de las ofertas.

---

## 4. Política de versionado de datos

Los CSV generados no están versionados en Git por defecto.

Como excepción práctica para el despliegue del dashboard, el repositorio incluye únicamente los CSV procesados finales necesarios para ejecutar la aplicación:

- `data/processed/job_postings_enriched.csv`
- `data/processed/ine_salary_context_processed.csv`
- `data/processed/manfred_salary_reference_processed.csv`

El resto de datos raw, intermedios o generados durante el proceso siguen excluidos de Git mediante `.gitignore`.

La carpeta `data/` conserva su estructura mediante archivos `.gitkeep`.

Esto permite mantener separadas las siguientes capas:

- datos raw;
- datos intermedios;
- datos procesados finales necesarios para despliegue;
- código fuente;
- documentación metodológica.

La decisión evita subir al repositorio archivos raw, intermedios o potencialmente pesados, pero permite que el dashboard desplegado funcione sin ejecutar scraping ni procesos largos de generación de datos.

Para reproducir el proyecto localmente, los datasets pueden regenerarse mediante los scripts incluidos en el repositorio.

---

## 5. Flujo reproducible de generación de datos

### 5.1 Comprobación de fuentes

Script:

```bash
python src/extraction/check_sources.py
```

Objetivo:

Comprobar que las fuentes principales están disponibles y que el proyecto puede continuar con la extracción.

---

### 5.2 Recogida de URLs candidatas

Script:

```bash
python src/extraction/collect_candidate_job_urls.py
```

Genera:

```text
data/raw/tecnoempleo_candidate_urls.csv
data/raw/ticjob_candidate_urls.csv
data/interim/job_urls.csv
```

Objetivo:

Construir una lista inicial de URLs candidatas de ofertas desde las fuentes seleccionadas.

---

### 5.3 Extracción y normalización de ofertas

Script:

```bash
python src/extraction/extract_job_postings_from_urls.py
```

Genera:

```text
data/interim/job_postings_normalized.csv
data/interim/job_postings_extraction_errors.csv
```

Objetivo:

Extraer datos estructurados de las ofertas, normalizar campos principales y registrar errores de extracción.

Los errores de extracción se conservan para poder auditar qué URLs no pudieron procesarse correctamente.

---

### 5.4 Enriquecimiento del dataset principal

Script:

```bash
python src/features/enrich_job_postings.py
```

Genera:

```text
data/processed/job_postings_enriched.csv
```

Objetivo:

Añadir variables útiles para el análisis y el dashboard, entre ellas:

- modalidad de trabajo estimada;
- seniority estimado;
- tecnologías detectadas;
- categoría profesional aproximada;
- normalización de país;
- tipo de dato salarial.

El enriquecimiento se basa en reglas y debe interpretarse como aproximación, no como clasificación perfecta.

---

### 5.5 Preparación del contexto salarial INE

Script:

```bash
python src/processing/prepare_ine_salary_context.py
```

Genera:

```text
data/processed/ine_salary_context_processed.csv
```

Objetivo:

Transformar la tabla oficial del INE en un dataset local preparado para lectura contextual dentro del dashboard.

---

### 5.6 Preparación de la referencia salarial Manfred

Script:

```bash
python src/processing/prepare_manfred_salary_reference.py
```

Genera:

```text
data/processed/manfred_salary_reference_processed.csv
```

Objetivo:

Transformar las tablas salariales de Manfred en una referencia estructurada por rol y nivel de experiencia.

---

## 6. Variables principales del dataset de ofertas

Columnas especialmente relevantes para el dashboard:

| Columna | Uso |
| --- | --- |
| `source` | Identificar portal de origen. |
| `url` | Trazabilidad de la oferta original. |
| `title` | Título de la oferta. |
| `company` | Empresa publicada en la oferta. |
| `date_posted` | Análisis temporal. |
| `location_locality` | Localidad publicada. |
| `location_region` | Región publicada. |
| `work_mode` | Modalidad estimada: remoto, híbrido, presencial o desconocido. |
| `seniority` | Nivel de experiencia estimado. |
| `technologies_detected` | Tecnologías detectadas mediante reglas. |
| `role_category` | Categoría profesional aproximada. |
| `description_length` | Nivel de detalle de la descripción. |
| `salary_offer_min` | Salario mínimo publicado si existe. |
| `salary_offer_max` | Salario máximo publicado si existe. |
| `salary_offer_avg` | Salario medio de la oferta cuando hay rango publicado. |
| `salary_data_type` | Indica si el salario está publicado o no disponible. |

---

## 7. Variables numéricas y categóricas

El dataset contiene variables suficientes para un análisis descriptivo profundo.

Variables numéricas utilizadas:

- `salary_offer_min`;
- `salary_offer_max`;
- `salary_offer_avg`;
- `description_length`.

Variables categóricas utilizadas:

- `source`;
- `role_category`;
- `work_mode`;
- `seniority`;
- `location_region`;
- `technologies_detected`;
- `salary_data_type`.

---

## 8. Criterios de filtrado temporal

El dataset procesado final se centra en ofertas de 2026.

Esta decisión se toma porque la extracción original contenía algunas filas antiguas, pero la mayor parte del volumen útil y actual se concentra en 2026.

Usar el filtro temporal permite que el dashboard represente mejor una lectura actual del mercado tecnológico español dentro de la muestra disponible.

---

## 9. Tratamiento de salarios

La política salarial del proyecto es conservadora:

- no se inventan salarios;
- no se imputan salarios ausentes;
- no se rellenan salarios con referencias externas;
- solo se analizan salarios publicados explícitamente en las ofertas;
- la baja disponibilidad salarial se interpreta como transparencia salarial, no como salario medio real del mercado.

En el dataset principal local, solo 28 de 2.240 ofertas tienen salario publicado.

Por este motivo, cualquier gráfico salarial basado en ofertas debe leerse como una muestra parcial y no representativa.

---

## 10. Enriquecimiento y clasificación

El dataset se enriquece mediante reglas aplicadas sobre campos como título, descripción y texto disponible.

Se generan variables como:

- `role_category`;
- `work_mode`;
- `seniority`;
- `technologies_detected`.

Estas variables facilitan el storytelling y la exploración del dashboard, pero tienen limitaciones.

Por ejemplo:

- una oferta puede pertenecer parcialmente a más de una categoría;
- algunas ofertas tienen títulos ambiguos;
- algunas descripciones no explicitan seniority o modalidad;
- algunas tecnologías pueden aparecer en la descripción sin ser el requisito principal;
- la categoría `Other` agrupa roles heterogéneos que no encajan claramente en las reglas principales.

Por tanto, las categorías deben interpretarse como aproximaciones analíticas.

---

## 11. Sesgos y limitaciones

### 11.1 Sesgo de fuente

El dataset procede solo de Tecnoempleo y Ticjob.

Esto implica que no representa todo el mercado laboral tecnológico español.

No incluye de forma completa ofertas publicadas en LinkedIn, InfoJobs, portales corporativos, consultoras, ETTs, comunidades técnicas u otras fuentes.

---

### 11.2 Sesgo de volumen por fuente

Tecnoempleo tiene mucho más peso que Ticjob en la muestra.

Distribución local:

| Fuente | Ofertas |
| --- | ---: |
| Tecnoempleo | 2.128 |
| Ticjob | 112 |

Esto puede influir en la distribución de perfiles, tecnologías, modalidades y ubicaciones.

---

### 11.3 Sesgo de clasificación

Las categorías profesionales se asignan mediante reglas.

Distribución local de `role_category`:

| Categoría | Ofertas |
| --- | ---: |
| Other | 1.019 |
| Backend | 401 |
| Data | 171 |
| SAP/ERP | 142 |
| DevOps | 128 |
| Cybersecurity | 104 |
| Frontend | 79 |
| Systems | 79 |
| Fullstack | 74 |
| QA | 43 |

La categoría `Other` no debe interpretarse como ruido puro. Puede contener perfiles funcionales, gestión, SAP no detectado inicialmente, consultoría, soporte, producto u otros perfiles técnicos o mixtos.

---

### 11.4 Sesgo de modalidad de trabajo

La modalidad de trabajo no siempre aparece de forma explícita en las ofertas.

Distribución local:

| Modalidad | Ofertas |
| --- | ---: |
| hybrid | 887 |
| unknown | 763 |
| remote | 458 |
| onsite | 132 |

La categoría `unknown` debe analizarse con cautela, ya que puede incluir ofertas donde la modalidad no está claramente indicada.

---

### 11.5 Sesgo de seniority

El seniority se estima mediante reglas y muchas ofertas no indican claramente el nivel requerido.

Distribución local:

| Seniority | Ofertas |
| --- | ---: |
| unknown | 1.644 |
| senior | 436 |
| junior | 93 |
| lead | 59 |
| mid | 8 |

Esto limita la posibilidad de sacar conclusiones fuertes sobre demanda real por nivel de experiencia.

---

### 11.6 Sesgo salarial

La disponibilidad salarial es muy baja.

Distribución local:

| Tipo de dato salarial | Ofertas |
| --- | ---: |
| unavailable | 2.212 |
| published_in_offer | 28 |

Esta limitación es central en el proyecto.

El dashboard no debe responder “cuál es el salario medio real del mercado”, sino “cuánta transparencia salarial hay en la muestra y cómo se compara con fuentes externas de contexto”.

---

## 12. Gobernanza y riesgos de interpretación

El dashboard debe usarse como herramienta exploratoria, no como fuente única de decisión.

Riesgos si se ignoran los sesgos:

- asumir que la muestra representa todo el mercado tecnológico español;
- tomar decisiones salariales usando solo las 28 ofertas con salario publicado;
- interpretar la ausencia de salario como salario bajo o inexistente;
- mezclar salarios sectoriales del INE con salarios específicos por rol tecnológico;
- usar Manfred como si fueran salarios observados directamente en las ofertas;
- considerar exactas categorías que son aproximaciones basadas en reglas;
- tomar decisiones de contratación, formación o inversión sin contrastar con más fuentes.

---

## 13. Uso correcto del dashboard

Uso recomendado:

- explorar tendencias dentro de la muestra;
- identificar perfiles y tecnologías frecuentes;
- observar modalidad de trabajo y distribución geográfica;
- detectar limitaciones de transparencia salarial;
- apoyar una conversación ejecutiva sobre mercado tech, datos y sesgos.

Uso no recomendado:

- estimar el salario medio real del mercado tecnológico español;
- decidir bandas salariales únicamente con este dataset;
- generalizar resultados a todo el mercado;
- automatizar decisiones de negocio sin revisión humana;
- sustituir análisis de mercado profesional con este único dashboard.

---

## 14. Relación con el storytelling del proyecto

La estrategia de datos está alineada con el objetivo narrativo del dashboard.

La historia principal del proyecto es:

> La muestra permite explorar demanda tecnológica en España, pero también muestra límites importantes de transparencia salarial, representatividad y calidad de información publicada.

Por eso el dashboard combina:

- métricas descriptivas;
- visualizaciones interactivas;
- filtros de segmentación;
- contexto salarial externo;
- advertencias metodológicas;
- recomendaciones operativas.

---

## 15. Reproducibilidad

El proyecto busca ser reproducible mediante scripts versionados.

Orden recomendado:

```bash
python src/extraction/check_sources.py
python src/extraction/collect_candidate_job_urls.py
python src/extraction/extract_job_postings_from_urls.py
python src/features/enrich_job_postings.py
python src/processing/prepare_ine_salary_context.py
python src/processing/prepare_manfred_salary_reference.py
streamlit run app.py
```

Los datos generados localmente pueden variar en el futuro si las fuentes cambian, eliminan ofertas o modifican su estructura.

Por ese motivo, las cifras documentadas corresponden a la versión local procesada durante el desarrollo del proyecto.

---

## 16. Mejoras futuras

Posibles mejoras metodológicas:

- añadir más fuentes de ofertas;
- separar mejor la categoría `Other`;
- mejorar la detección de seniority;
- validar manualmente una muestra de clasificaciones;
- registrar fecha exacta de extracción en metadatos;
- añadir tests automáticos para reglas de enriquecimiento;
- comparar resultados con portales adicionales;
- documentar una validación con usuario no técnico;
- añadir capturas o evidencias del despliegue cuando exista URL pública.

---

## 17. Conclusión

La estrategia de datos del proyecto prioriza una lectura honesta y trazable.

El valor principal no está en afirmar que la muestra representa todo el mercado, sino en mostrar cómo un dashboard puede convertir datos imperfectos en una narrativa ejecutiva útil, siempre que se expliquen sus límites, sesgos y riesgos de interpretación.
