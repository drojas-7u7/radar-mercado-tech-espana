# Estrategia de datos

## Tema del proyecto

El proyecto analiza una muestra de ofertas del mercado laboral tecnológico en España mediante un dashboard interactivo centrado en ofertas de empleo, perfiles profesionales, tecnologías demandadas, modalidad de trabajo, publicación de salarios y limitaciones de los datos.

El proyecto no pretende representar de forma absoluta todo el mercado tecnológico español. Su objetivo es construir una lectura exploratoria y defendible a partir de fuentes reales, explicando claramente el alcance, los sesgos y las limitaciones.

## Objetivo principal

Transformar datos brutos y semiestructurados del mercado laboral tecnológico en España en conclusiones claras para una audiencia no técnica.

El dashboard debe ayudar a responder preguntas como:

- qué tipos de perfiles aparecen con más frecuencia en la muestra
- qué tecnologías se repiten más en las ofertas
- qué modalidades de trabajo se detectan
- qué nivel de transparencia salarial existe en las ofertas
- qué limitaciones aparecen al trabajar con datos reales extraídos de portales de empleo

## Dataset principal del proyecto

### 1. Tecnoempleo

Propósito: fuente principal para obtener ofertas tecnológicas actuales en España.

Uso dentro del proyecto:

- fuente principal del dataset de ofertas
- extracción de URLs candidatas
- extracción de información estructurada desde ofertas reales
- normalización y enriquecimiento posterior

Campos utilizados o derivados:

- source
- url
- title
- company
- date_posted
- valid_through
- employment_type
- salary_offer_min
- salary_offer_max
- salary_offer_avg
- salary_data_type
- description
- description_length
- location_locality
- location_region
- location_country
- work_mode
- seniority
- technologies_detected
- role_category

Estado: validado técnicamente e integrado como fuente principal.

Limitación principal: Tecnoempleo domina el dataset final, por lo que las conclusiones deben presentarse como una muestra extraída principalmente de este portal, no como una representación completa de todo el mercado.

### 2. Ticjob

Propósito: fuente secundaria para complementar el dataset principal con ofertas tecnológicas actuales en España.

Uso dentro del proyecto:

- fuente secundaria de ofertas
- complemento para reducir la dependencia de una única fuente
- comparación parcial frente a Tecnoempleo

Campos utilizados o derivados:

- source
- url
- title
- company
- date_posted
- valid_through
- employment_type
- salary_offer_min
- salary_offer_max
- salary_offer_avg
- salary_data_type
- description
- description_length
- location_locality
- location_region
- location_country
- work_mode
- seniority
- technologies_detected
- role_category

Estado: validado técnicamente e integrado como fuente secundaria.

Limitación principal: su peso en el dataset final es mucho menor que el de Tecnoempleo, por lo que no equilibra completamente la muestra.

## Dataset procesado actual

El dataset principal procesado del dashboard es:

```text
data/processed/job_postings_enriched.csv
```

Estado actual del dataset:

```text
Filas: 2240
Columnas: 23
Rango temporal: 2026-01-02 a 2026-06-15
Fuente principal: Tecnoempleo
Fuente secundaria: Ticjob
```

Distribución por fuente:

```text
Tecnoempleo: 2128
Ticjob: 112
```

El dataset procesado se filtró para conservar ofertas publicadas desde 2026-01-01, con el objetivo de representar una fotografía reciente del mercado.

## Fuentes externas previstas

### 3. Referencia salarial tech España 2026

Propósito: aportar una referencia salarial externa y específica del sector tecnológico en España.

Fuente recomendada:

```text
Guía Salarial 2026 - Salarios en tecnología [España] - Manfred
```

Motivo de uso:

El dataset principal contiene muy pocas ofertas con salario publicado. Por tanto, una referencia salarial externa puede ayudar a contextualizar rangos salariales por rol, siempre separándola claramente de los salarios observados en las ofertas.

Uso permitido:

* contexto salarial por rol tecnológico
* comparación general con los pocos salarios publicados
* apoyo narrativo para explicar la baja transparencia salarial
* referencia separada del dataset principal de ofertas

Uso no permitido:

* no rellenar salarios ausentes en las ofertas
* no presentar referencias externas como salarios reales de cada oferta
* no calcular medias del mercado mezclando salarios publicados y referencias externas como si fueran el mismo tipo de dato

Estado: fuente prioritaria pendiente de integración.

Posible salida procesada:

```text
data/processed/salary_reference_tech_2026_processed.csv
```

Posible script de preparación:

```text
src/processing/prepare_salary_reference.py
```

### 4. INE / datos.gob.es

Propósito: aportar contexto oficial sobre salarios y empleo en España.

Fuentes recomendadas:

```text
INE - Encuesta Anual de Estructura Salarial
datos.gob.es - datasets de salarios medios del INE
```

Uso permitido:

* contexto institucional
* comparación con salarios generales en España
* apoyo a la sección de limitaciones
* explicación de que las ofertas tecnológicas no representan todo el mercado laboral
* comparación general, no específica por oferta

Uso no permitido:

* no usar datos generales del INE como salario tech por rol
* no mezclar indicadores oficiales generales con salarios de ofertas como si fueran equivalentes
* no usarlos para rellenar salarios ausentes

Estado: fuente contextual recomendada, pendiente de integración.

Posible salida procesada:

```text
data/processed/ine_salary_context_processed.csv
```

Posible script de preparación:

```text
src/processing/prepare_ine_context.py
```

### 5. Dataset externo de ofertas de empleo en España

Propósito: servir como dataset de respaldo o comparación si se quiere contrastar la muestra propia con otra fuente externa.

Uso permitido:

* comparación metodológica
* plan B si el scraping propio fuera insuficiente
* apoyo en README o limitaciones

Uso no recomendado por ahora:

* sustituir el dataset principal propio
* mezclarlo directamente con Tecnoempleo/Ticjob sin una normalización cuidadosa
* convertirlo en el eje principal del dashboard

Estado: plan B o comparación opcional.

### 6. Dataset internacional de salarios Data/AI

Propósito: posible benchmark secundario para roles de datos/IA.

Uso permitido:

* comparación internacional secundaria
* contexto opcional si aporta valor narrativo claro

Uso no recomendado por ahora:

* usarlo como referencia principal
* compararlo directamente con ofertas españolas sin explicar diferencias de país, moneda, seniority, modalidad y fuente

Estado: opcional y de baja prioridad.

## Política sobre datos salariales

El proyecto separará la información salarial en diferentes tipos de dato:

* salary_offer_min: salario mínimo publicado explícitamente en una oferta
* salary_offer_max: salario máximo publicado explícitamente en una oferta
* salary_offer_avg: salario medio estimado solo a partir del rango publicado en la oferta
* salary_reference_avg: referencia salarial externa por tipo de rol, si se integra una fuente externa
* salary_data_type: tipo de dato salarial

Valores esperados de salary_data_type:

* published_in_offer: salario publicado explícitamente en la oferta
* reference_by_role: referencia externa por rol, si se integra
* unavailable: salario no disponible

Reglas:

* no se inventarán salarios ausentes
* no se imputarán salarios oferta por oferta
* no se mezclarán salarios publicados y referencias externas como si fueran equivalentes
* las referencias externas se mostrarán separadas de los salarios publicados
* la baja publicación de salarios se tratará como una conclusión relevante sobre transparencia salarial

Estado salarial actual del dataset principal:

```text
published_in_offer: 28
unavailable: 2212
```

## Política sobre categorías y variables derivadas

### role_category

La variable role_category es una clasificación aproximada basada en reglas.

Estado actual de categorías:

```text
Other
Backend
Data
SAP/ERP
DevOps
Cybersecurity
Frontend
Systems
Fullstack
QA
```

Limitación:

La clasificación no es perfecta. Algunos perfiles mixtos, ambiguos o mal descritos pueden quedar en Other o en una categoría aproximada.

Regla narrativa:

role_category debe presentarse como una clasificación exploratoria y transparente, no como una taxonomía oficial del mercado laboral.

### work_mode

La variable work_mode se deriva de la información disponible en la oferta.

Valores actuales:

```text
hybrid
remote
onsite
unknown
```

Limitación:

Muchas ofertas no indican claramente la modalidad. Por tanto, las conclusiones sobre remoto/híbrido deben expresarse con cautela.

### seniority

La variable seniority se deriva mediante reglas aproximadas.

Valores actuales:

```text
unknown
senior
junior
lead
mid
```

Limitación:

La mayoría de ofertas no permite detectar seniority con seguridad. Por tanto, seniority debe usarse como señal exploratoria, no como conclusión central.

### technologies_detected

La variable technologies_detected se deriva a partir de palabras clave detectadas en el texto de la oferta.

Limitación:

Una tecnología puede aparecer como requisito obligatorio, deseable, herramienta secundaria o simple mención. Por tanto, el dashboard debe hablar de tecnologías mencionadas o detectadas, no necesariamente de requisitos obligatorios.

## Estrategia modular de integración

Las fuentes externas no deben integrarse directamente en app.py.

Flujo recomendado:

```text
data/raw/
    fuente_original.csv

src/processing/ o src/features/
    script_de_preparacion.py

data/processed/
    fuente_procesada.csv

app.py
    consume solo datos procesados
```

El dashboard debe mantenerse como capa de visualización e interacción, no como lugar de scraping, limpieza o transformación pesada.

## Consideraciones de gobernanza y sesgos

Limitaciones principales:

* los portales de empleo no representan todo el mercado laboral
* Tecnoempleo está sobrerrepresentado frente a Ticjob
* el dataset está concentrado temporalmente en el primer semestre de 2026
* muchas empresas no publican rangos salariales
* la muestra de salarios publicados es muy pequeña
* algunas ofertas pueden estar duplicadas entre portales, aunque actualmente no se han detectado duplicados por URL en el dataset validado
* algunas ofertas pueden etiquetarse como junior aunque pidan experiencia intermedia
* muchas ofertas no permiten detectar seniority con seguridad
* muchas ofertas no indican claramente la modalidad de trabajo
* las tecnologías detectadas pueden aparecer como requisitos deseables y no obligatorios
* role_category es una clasificación basada en reglas y puede contener errores
* algunas regiones, empresas o portales pueden estar sobrerrepresentados
* el dataset representa una fotografía temporal, no una tendencia histórica completa
* los datos oficiales del INE/datos.gob.es, si se integran, aportan contexto general, no equivalencia directa con salarios tech por rol

Estas limitaciones deberán mostrarse de forma clara en el dashboard, explicarse en el README y mencionarse en la presentación final.
