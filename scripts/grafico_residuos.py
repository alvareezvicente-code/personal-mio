from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
GRAFICOS_DIR = BASE_DIR / "graficos"
DATA_DIR.mkdir(exist_ok=True)
GRAFICOS_DIR.mkdir(exist_ok=True)
ARCHIVOS = sorted(DATA_DIR.glob("residuos_*.csv"))

partes = []
for archivo in ARCHIVOS:
    # El recurso 2026 actualmente contiene solo las palabras "datos/vacio".
    if archivo.stat().st_size < 100:
        continue

    datos = pd.read_csv(archivo, usecols=["fecha_dia", "peso_neto"])
    usa_barras = datos["fecha_dia"].astype(str).str.contains("/", regex=False)
    fechas = pd.Series(pd.NaT, index=datos.index, dtype="datetime64[ns]")
    fechas.loc[usa_barras] = pd.to_datetime(
        datos.loc[usa_barras, "fecha_dia"], format="%d/%m/%y %H:%M", errors="coerce"
    )
    fechas.loc[~usa_barras] = pd.to_datetime(
        datos.loc[~usa_barras, "fecha_dia"], format="%Y-%m-%d", errors="coerce"
    )
    datos["fecha_dia"] = fechas
    datos["peso_neto"] = pd.to_numeric(datos["peso_neto"], errors="coerce")
    partes.append(datos.dropna())

if not partes:
    raise ValueError("No se encontraron CSV con datos válidos.")

df = pd.concat(partes, ignore_index=True)
df["anio"] = df["fecha_dia"].dt.year
df["mes"] = df["fecha_dia"].dt.month

mensual = (
    df.groupby(["anio", "mes"], as_index=False)["peso_neto"].sum()
    .assign(toneladas=lambda x: x["peso_neto"] / 1000)
)

salida = GRAFICOS_DIR / "grafico_residuos_mensuales.png"
ancho, alto = 1500, 850
margen_izq, margen_der, margen_sup, margen_inf = 145, 90, 120, 145
x0, x1 = margen_izq, ancho - margen_der
y0, y1 = margen_sup, alto - margen_inf
imagen = Image.new("RGB", (ancho, alto), "white")
dibujo = ImageDraw.Draw(imagen)

fuente_regular = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
fuente_chica = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 19)
fuente_titulo = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)

maximo = mensual["toneladas"].max()
tope = ((int(maximo) // 500) + 1) * 500
colores = {2023: "#2F6690", 2024: "#E76F51", 2025: "#2A9D8F"}
meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

def coord_x(mes):
    return x0 + (mes - 1) * (x1 - x0) / 11

def coord_y(valor):
    return y1 - valor * (y1 - y0) / tope

dibujo.text((margen_izq, 42), "Residuos recibidos en la Estación de Transferencia", fill="#202124", font=fuente_titulo)
for valor in range(0, tope + 1, 500):
    y = coord_y(valor)
    dibujo.line((x0, y, x1, y), fill="#D9DEE3", width=2)
    etiqueta = f"{valor:,}".replace(",", ".")
    dibujo.text((x0 - 18, y), etiqueta, fill="#555555", font=fuente_chica, anchor="rm")

dibujo.line((x0, y0, x0, y1), fill="#60656B", width=3)
dibujo.line((x0, y1, x1, y1), fill="#60656B", width=3)
for mes, etiqueta in enumerate(meses, 1):
    x = coord_x(mes)
    dibujo.text((x, y1 + 18), etiqueta, fill="#444444", font=fuente_chica, anchor="ma")

for anio, datos_anio in mensual.groupby("anio"):
    puntos = [(coord_x(fila.mes), coord_y(fila.toneladas)) for fila in datos_anio.itertuples()]
    color = colores.get(anio, "#7A5195")
    if len(puntos) > 1:
        dibujo.line(puntos, fill=color, width=6, joint="curve")
    for x, y in puntos:
        dibujo.ellipse((x - 8, y - 8, x + 8, y + 8), fill=color, outline="white", width=3)

dibujo.text((x0, y0 - 18), "Peso neto (toneladas)", fill="#333333", font=fuente_chica, anchor="ls")
leyenda_x = x1 - 280
for indice, anio in enumerate(sorted(mensual["anio"].unique())):
    x = leyenda_x + indice * 105
    dibujo.line((x, 83, x + 34, 83), fill=colores.get(anio, "#7A5195"), width=6)
    dibujo.text((x + 43, 83), str(anio), fill="#333333", font=fuente_chica, anchor="lm")

nota = ("Fuente: Intendencia de Montevideo. 2023 comienza en noviembre; "
        "2025 llega hasta agosto; 2026 todavía no contiene datos.")
dibujo.text((margen_izq, alto - 55), nota, fill="#666666", font=fuente_chica)
imagen.save(salida, quality=95)
print(f"Gráfico guardado en: {salida}")
print("\nToneladas por año disponibles:")
print((df.groupby("anio")["peso_neto"].sum() / 1000).round(2))