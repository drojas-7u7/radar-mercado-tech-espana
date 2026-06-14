# Estrategia de datos

## Tema del proyecto

El proyecto analiza el mercado laboral tecnológico en España mediante un dashboard interactivo centrado en ofertas de empleo, perfiles profesionales, tecnologías demandadas, modalidad de trabajo, ubicación y transparencia salarial.

## Objetivo principal

Transformar datos brutos y semiestructurados del mercado laboral tecnológico en conclusiones claras para una audiencia no técnica.

## Fuentes de datos previstas

### 1. Tecnoempleo

Propósito: fuente principal para obtener ofertas tecnológicas actuales en España.

Campos esperados:

- título de la oferta
- empresa
- ubicación
- modalidad de trabajo
- salario, si está disponible
- tecnologías o palabras clave
- fecha de publicación, si está disponible
- URL de la oferta

Estado: pendiente de validación técnica.

### 2. Ticjob

Propósito: fuente secundaria para obtener ofertas tecnológicas actuales en España.

Campos esperados:

- título de la oferta
- empresa
- ubicación
- modalidad de trabajo
- salario, si está disponible
- tecnologías o palabras clave
- fecha de publicación, si está disponible
- URL de la oferta

Estado: pendiente de validación técnica.

### 3. Fuente de referencia salarial

Propósito: aportar una referencia salarial más sólida, ya que muchas ofertas extraídas mediante scraping pueden no incluir salario.

Nota importante: las referencias salariales no deben presentarse como salarios exactos de cada oferta. Deben separarse claramente de los salarios publicados explícitamente en las ofertas.

Estado: pendiente de validación de fuente.

### 4. datos.gob.es / INE

Propósito: aportar contexto oficial sobre empleo o salarios en España.

Posibles usos:

- comparar referencias salariales tecnológicas con indicadores salariales generales en España
- añadir contexto institucional
- reforzar la sección de gobernanza y limitaciones del análisis

Estado: pendiente de validación de fuente.

### 5. Dataset de ofertas de empleo en España

Propósito: servir como dataset de respaldo o comparación si el scraping resulta limitado o incompleto.

Estado: pendiente de validación del dataset.

## Política sobre datos salariales

El proyecto separará la información salarial en diferentes campos:

- salary_offer_min: salario mínimo publicado explícitamente en una oferta
- salary_offer_max: salario máximo publicado explícitamente en una oferta
- salary_offer_avg: salario medio estimado a partir del rango publicado en la oferta
- salary_reference_avg: referencia salarial externa por tipo de rol
- salary_data_type: published_in_offer, reference_by_role o unavailable

No se inventarán salarios ausentes.

## Consideraciones de gobernanza y sesgos

Posibles limitaciones:

- los portales de empleo no representan todo el mercado laboral
- muchas empresas no publican rangos salariales
- algunas ofertas pueden estar duplicadas entre portales
- algunas ofertas pueden etiquetarse como junior aunque pidan experiencia intermedia
- las tecnologías detectadas pueden aparecer como requisitos deseables y no obligatorios
- el dataset representará una fotografía temporal, no una tendencia histórica completa
- algunas regiones, empresas o portales pueden estar sobrerrepresentados

Estas limitaciones deberán mostrarse de forma clara en el dashboard y explicarse en el README.
