# Estrategia de datos

Documento pendiente de actualización final.

La estrategia real y actual del proyecto se está consolidando en el código, los scripts reproducibles y los datasets generados localmente. Este documento se actualizará al final del proyecto para evitar mantener información intermedia desactualizada.

## Fuentes actualmente procesadas

- **Ofertas tech en España**: dataset principal construido a partir de Tecnoempleo y Ticjob.
- **INE 66245**: contexto oficial sectorial sobre salario mensual bruto por rama de actividad.
- **Manfred 2026**: referencia salarial tecnológica por rol y rango de experiencia.

## Criterios metodológicos confirmados

- No se inventan datos.
- No se imputan salarios ausentes.
- Los salarios publicados en ofertas se analizan únicamente cuando aparecen explícitamente.
- INE y Manfred se usan como fuentes complementarias de contexto.
- INE y Manfred no sustituyen al dataset principal de ofertas.
- Todas las fuentes externas deben poder regenerarse mediante scripts reproducibles.

## Pendiente

Actualizar esta documentación al final del proyecto con:

- fuentes definitivas;
- scripts usados;
- limitaciones;
- sesgos;
- criterios de filtrado;
- explicación de columnas principales;
- metodología de scraping, enriquecimiento y visualización.
