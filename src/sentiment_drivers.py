"""Las tres figuras del README, en SVG y desde los datos reales.

Complementa a `src/sentiment_analysis.py`, que genera el conjunto
 exploratorio en PNG y `outputs/insights.md`. Este módulo hace solo lo que
el README necesita, en texto plano para que GitHub lo muestre nítido.

Uso: python src/sentiment_drivers.py
"""
import pathlib
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from svg_chart import AZUL, ROJO, barras

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "reviews_sentiment_TRANSFORMADO_ROBUSTO_100k.csv"
IMG, OUT = ROOT / "docs" / "img", ROOT / "outputs"
IMG.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

d = pd.read_csv(RAW)
print(f"1. cargado: {len(d):,} reseñas · {d.product_id.nunique():,} productos")

cuenta = d["sentiment_category"].value_counts()
neg_pct = cuenta.get("Negative", 0) / len(d)
print("2. sentimiento:", {k: int(v) for k, v in cuenta.items()},
      f"· negativas {neg_pct:.1%}")

barras(
    [(k, v / len(d) * 100, ROJO if k == "Negative" else AZUL)
     for k, v in cuenta.reindex(["Positive", "Neutral", "Negative"]).items()],
    "Nueve de cada diez reseñas son positivas",
    IMG / "sent-mix.svg",
    subtitulo=f"{len(d):,} reseñas de {d.product_id.nunique():,} productos · % del total",
    formato="{:.1f}", sufijo="%")

por_nota = d.groupby("rating")["sentiment_category"].agg(
    positivas=lambda s: (s == "Positive").mean(), n="size")
print("\n3. % de sentimiento positivo por nota:")
print((por_nota["positivas"] * 100).round(1).to_string())

barras(
    [(f"{int(r)} estrella" + ("s" if r > 1 else ""), v * 100, ROJO if r <= 2 else AZUL)
     for r, v in por_nota["positivas"].items()],
    "El texto no sigue a la nota",
    IMG / "sent-conflicto.svg",
    subtitulo="% de reseñas con sentimiento positivo, por nota de la reseña",
    formato="{:.1f}", sufijo="%")

por_producto = d.groupby("product_id").agg(
    n=("Id", "size"),
    negativas=("sentiment_category", lambda s: (s == "Negative").mean()))
con_volumen = por_producto[por_producto["n"] >= 20].sort_values("negativas",
                                                               ascending=False)
peores = con_volumen.head(8)
print(f"\n4. {len(por_producto):,} productos · {len(con_volumen)} con 20+ reseñas")
print(peores.round(3).to_string())

barras(
    [(i, v * 100, ROJO) for i, v in peores["negativas"].items()],
    "Productos donde el rechazo es la norma",
    IMG / "sent-productos.svg",
    subtitulo=f"% de reseñas negativas · productos con 20 o más reseñas · media global {neg_pct:.1%}",
    formato="{:.1f}", sufijo="%")

por_nota.to_csv(OUT / "sentiment_by_rating.csv")
con_volumen.head(50).to_csv(OUT / "worst_products.csv")
print("\n5. media de compound por nota:")
print(d.groupby("rating")["compound_score"].mean().round(3).to_string())
uno = d.rating == 1
print(f"\nreseñas de 1 estrella: {int(uno.sum()):,} · con sentimiento positivo: "
      f"{int((uno & (d.sentiment_category == 'Positive')).sum()):,} "
      f"({(uno & (d.sentiment_category == 'Positive')).sum() / uno.sum():.1%})")
