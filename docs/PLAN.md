# Plan de ejecucion

## Estado actual
- 100.000 resenas puntuadas con VADER (compound_score y categorias) versionadas y validadas por CI.
- `top_negative_products.csv` con 12 productos priorizados por tasa negativa.
- Informe en `docs/report.html` y workflow de triage con LLM en `automation/n8n/`.

## Proximos pasos
1. Etiquetar a mano 500 resenas y contrastar VADER vs LLM (matriz de confusion).
2. Reducir el CSV de 4,5 MB a una muestra de 10k + enlace de descarga.
3. Test de rango: `compound_score` debe estar en [-1, 1].
4. Publicar las acciones del LLM en un tablero (Notion o Sheet).

## Criterio de aceptacion
- Ninguna fila fuera de rango; el workflow de n8n devuelve JSON valido o falla ruidosamente.

## Riesgos
- VADER no entiende sarcasmo ni espanol: el LLM complementa, no reemplaza.
