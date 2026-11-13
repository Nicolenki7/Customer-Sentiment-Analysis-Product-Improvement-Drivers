"""Construye docs/report.html del análisis de sentimiento de reseñas Amazon.

Uso: python src/build_report.py
"""
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from report import escribir, num

ROOT = pathlib.Path(__file__).resolve().parents[1]
d = pd.read_csv(ROOT / "reviews_sentiment_TRANSFORMADO_ROBUSTO_100k.csv")
top = pd.read_csv(ROOT / "outputs" / "top_negative_products.csv")

filas = []
for k, s in d.groupby("sentiment_category"):
    filas.append({"a": "todos", "g": "sentimiento", "k": str(k), "v": round(100 * len(s) / len(d), 1), "u": "%"})
for k, s in d.groupby("rating"):
    filas.append({"a": "todos", "g": "estrellas", "k": f"{int(k)} estrellas", "v": round(float(s.compound_score.mean()), 3), "u": ""})
    filas.append({"a": "todos", "g": "volumen", "k": f"{int(k)} estrellas", "v": int(len(s)), "u": ""})
for _, r in top.sort_values("neg_rate", ascending=False).head(8).iterrows():
    filas.append({"a": "todos", "g": "productos", "k": str(r.product_id), "v": round(100 * float(r.neg_rate), 1), "u": "%"})

tabla = [[str(r.product_id), num(int(r.n), 0), f"{num(100 * r.neg_rate, 1)} %", num(r.avg_rating, 2)]
         for _, r in top.sort_values("neg_rate", ascending=False).head(10).iterrows()]

escribir(
    ROOT / "docs" / "report.html",
    eyebrow="Voz del cliente · reseñas Amazon",
    titulo="Reseñas: dónde duele el producto",
    pregunta=("Cien mil reseñas con su polaridad calculada. La pregunta no es qué porcentaje es negativo, "
              "sino qué productos concentran el enfado y si las estrellas dicen lo mismo que el texto: "
              "cuando no coinciden, la nota media está escondiendo el problema."),
    kpis=[("Reseñas", num(len(d)), "con polaridad calculada"),
          ("Productos", num(d.product_id.nunique()), "identificadores distintos"),
          ("Negativas", f"{num(100 * (d.sentiment_category.astype(str).str.lower() == 'negative').mean(), 1)} %", "texto negativo"),
          ("Compound medio", num(d.compound_score.mean(), 3), "escala -1 a 1")],
    filtros=None,
    graficos=[
        {"id": "s", "grupo": "sentimiento", "titulo": "Reparto del sentimiento",
         "subtitulo": "% de reseñas en cada categoría del modelo", "unidad": "%"},
        {"id": "c", "grupo": "estrellas", "titulo": "Polaridad media por calificación",
         "subtitulo": "compound de VADER; -1 es lo más negativo", "unidad": ""},
        {"id": "v", "grupo": "volumen", "titulo": "Volumen por calificación",
         "subtitulo": "cuántas reseñas hay detrás de cada barra anterior", "unidad": ""},
        {"id": "p", "grupo": "productos", "titulo": "Productos con más reseñas negativas",
         "subtitulo": "% de sus reseñas que son negativas", "unidad": "%"},
    ],
    filas=filas,
    tabla={"titulo": "Los productos más castigados",
           "subtitulo": "ordenados por tasa de reseñas negativas",
           "cabeceras": ["Producto", "Reseñas", "Negativas", "Nota media"],
           "filas": tabla},
    metodo=["Cada fila es una reseña; la polaridad ya viene calculada en el CSV (compound de VADER).",
            "La tasa negativa de un producto es reseñas negativas / reseñas de ese producto, no / total.",
            "Los productos de la tabla son los que aparecen en outputs/top_negative_products.csv del proyecto.",
            "No se recalculan sentimientos: se agrega la columna que produjo el pipeline de NLP."],
    limitaciones=["El ranking solo mira productos con volumen suficiente en la muestra; el resto no aparece.",
                  "Una tasa negativa alta con pocas reseñas es ruido, no una señal.",
                  "VADER falla con ironía y sarcasmo, que en reseñas es habitual.",
                  "No hay fechas por reseña, así que no se puede ver si el problema es actual o viejo."],
    fuente="reviews_sentiment_TRANSFORMADO_ROBUSTO_100k.csv y outputs/top_negative_products.csv",
    metodo_sub="Una fila por reseña; el ranking de productos sale de un archivo aparte del proyecto.",
    lim_sub="Los cortes que este dataset no sostiene.")
print("docs/report.html:", (ROOT / "docs" / "report.html").stat().st_size, "bytes")
