from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


# =============================================================================
# 1. CONFIGURACIÓN Y DESCARGA DE LOS DATOS
# =============================================================================

BASE_DIR = Path(__file__).resolve().parent

URLS = {
    2023: "https://ckan-data.montevideo.gub.uy/dataset/f7662ff2-5962-45df-a085-0640813dc4cb/resource/3f9b098b-fb30-47c6-a367-911bb0d1bf49/download/cantidad_de_residuos_en_la_estacion_de_transferencia_2023.csv",
    2024: "https://ckan-data.montevideo.gub.uy/dataset/f7662ff2-5962-45df-a085-0640813dc4cb/resource/f7974b39-4a9a-40ff-a572-b786ff5cc1b0/download/cantidad_de_residuos_en_la_estacion_de_transferencia_2024.csv",
    2025: "https://ckan-data.montevideo.gub.uy/dataset/f7662ff2-5962-45df-a085-0640813dc4cb/resource/0102f60e-e1b5-404e-805d-81183447096e/download/cantidad_de_residuos_en_la_estacion_de_transferencia_2025.csv",
    2026: "https://ckan-data.montevideo.gub.uy/dataset/f7662ff2-5962-45df-a085-0640813dc4cb/resource/00ee3482-9b40-4df7-84fe-3baa7882faca/download/cantidad_de_residuos_en_la_estacion_de_transferencia_2026.csv",
}

archivos_validos = []

for anio, url in URLS.items():
    archivo = BASE_DIR / f"residuos_{anio}.csv"

    if not archivo.exists():
        print(f"Descargando datos de {anio}...")
        try:
            urlretrieve(url, archivo)
        except Exception as error:
            print(f"No se pudo descargar {anio}: {error}")
            continue

    # El recurso 2026 actualmente contiene solamente "datos/vacio".
    if archivo.stat().st_size < 100:
        print(f"El archivo de {anio} no contiene registros y será omitido.")
        continue

    archivos_validos.append((anio, archivo))

if not archivos_validos:
    raise FileNotFoundError("No se encontró ni se pudo descargar ningún CSV válido.")


# =============================================================================
# 2. CARGA Y UNIÓN DE LOS CSV
# =============================================================================

partes = []

for anio, archivo in archivos_validos:
    datos_anio = pd.read_csv(archivo, low_memory=False)
    datos_anio["anio_archivo"] = anio
    partes.append(datos_anio)
    print(f"{archivo.name}: {len(datos_anio):,} filas cargadas")

df = pd.concat(partes, ignore_index=True)

print("\n--- DATOS CARGADOS CORRECTAMENTE ---")
print(f"Archivos utilizados: {len(archivos_validos)}")
print(f"Dimensiones del conjunto unido: {df.shape[0]:,} filas x {df.shape[1]} columnas")


# =============================================================================
# 3. INSPECCIÓN INICIAL
# =============================================================================

print("\n--- INFORMACIÓN DEL DATAFRAME ---")
df.info()

print("\n--- PRIMERAS 5 FILAS ---")
print(df.head())

print("\n--- CANTIDAD DE VALORES ÚNICOS POR COLUMNA ---")
print(df.nunique(dropna=False).sort_values(ascending=False))

if "matricula_letra" in df.columns:
    print(f"\nMatrículas diferentes: {df['matricula_letra'].nunique()}")

print("\n--- DATOS FALTANTES POR COLUMNA ---")
faltantes = df.isnull().sum()
print(faltantes[faltantes > 0].sort_values(ascending=False))

print("\n--- CADENAS VACÍAS POR COLUMNA ---")
columnas_texto = df.select_dtypes(include=["object", "string"])
vacios = columnas_texto.eq("").sum()
print(vacios[vacios > 0].sort_values(ascending=False))

print(f"\nFilas exactamente duplicadas: {df.duplicated().sum():,}")


# =============================================================================
# 4. LIMPIEZA DE FECHAS Y PESO
# =============================================================================

# En 2023 las fechas tienen formato día/mes/año; desde 2024 usan año-mes-día.
usa_barras = df["fecha_dia"].astype(str).str.contains("/", regex=False)
fechas = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")

fechas.loc[usa_barras] = pd.to_datetime(
    df.loc[usa_barras, "fecha_dia"],
    format="%d/%m/%y %H:%M",
    errors="coerce",
)
fechas.loc[~usa_barras] = pd.to_datetime(
    df.loc[~usa_barras, "fecha_dia"],
    format="%Y-%m-%d",
    errors="coerce",
)

df["fecha_dia_limpia"] = fechas
df["peso_neto"] = pd.to_numeric(df["peso_neto"], errors="coerce")

df_grafico = df.dropna(subset=["fecha_dia_limpia", "peso_neto"]).copy()
df_grafico["anio"] = df_grafico["fecha_dia_limpia"].dt.year
df_grafico["mes"] = df_grafico["fecha_dia_limpia"].dt.month

mensual = (
    df_grafico.groupby(["anio", "mes"], as_index=False)["peso_neto"]
    .sum()
    .assign(toneladas=lambda tabla: tabla["peso_neto"] / 1000)
)

print("\n--- TONELADAS DISPONIBLES POR AÑO ---")
totales = df_grafico.groupby("anio")["peso_neto"].sum().div(1000).round(2)
print(totales)


# =============================================================================
# 5. GRÁFICO DE TONELADAS POR MES
# =============================================================================

salida = BASE_DIR / "grafico_residuos_mensuales.png"
ancho, alto = 1500, 850
margen_izq, margen_der, margen_sup, margen_inf = 145, 90, 120, 145
x0, x1 = margen_izq, ancho - margen_der
y0, y1 = margen_sup, alto - margen_inf

imagen = Image.new("RGB", (ancho, alto), "white")
dibujo = ImageDraw.Draw(imagen)

try:
    fuente_regular = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 19)
    fuente_titulo = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 36)
except OSError:
    fuente_regular = ImageFont.load_default()
    fuente_titulo = ImageFont.load_default()

maximo = mensual["toneladas"].max()
paso_y = 500
tope = max(paso_y, ((int(maximo) // paso_y) + 1) * paso_y)
colores = {2023: "#2F6690", 2024: "#E76F51", 2025: "#2A9D8F", 2026: "#7A5195"}
meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def coord_x(mes):
    return x0 + (mes - 1) * (x1 - x0) / 11


def coord_y(valor):
    return y1 - valor * (y1 - y0) / tope


dibujo.text(
    (margen_izq, 42),
    "Residuos recibidos en la Estación de Transferencia",
    fill="#202124",
    font=fuente_titulo,
)

for valor in range(0, tope + 1, paso_y):
    y = coord_y(valor)
    dibujo.line((x0, y, x1, y), fill="#D9DEE3", width=2)
    etiqueta = f"{valor:,}".replace(",", ".")
    dibujo.text((x0 - 18, y), etiqueta, fill="#555555", font=fuente_regular, anchor="rm")

dibujo.line((x0, y0, x0, y1), fill="#60656B", width=3)
dibujo.line((x0, y1, x1, y1), fill="#60656B", width=3)

for mes, etiqueta in enumerate(meses, 1):
    x = coord_x(mes)
    dibujo.text((x, y1 + 18), etiqueta, fill="#444444", font=fuente_regular, anchor="ma")

for anio, datos_anio in mensual.groupby("anio"):
    puntos = [
        (coord_x(fila.mes), coord_y(fila.toneladas))
        for fila in datos_anio.itertuples()
    ]
    color = colores.get(anio, "#7A5195")

    if len(puntos) > 1:
        dibujo.line(puntos, fill=color, width=6, joint="curve")

    for x, y in puntos:
        dibujo.ellipse(
            (x - 8, y - 8, x + 8, y + 8),
            fill=color,
            outline="white",
            width=3,
        )

dibujo.text(
    (x0, y0 - 18),
    "Peso neto (toneladas)",
    fill="#333333",
    font=fuente_regular,
    anchor="ls",
)

anios = sorted(mensual["anio"].unique())
leyenda_x = x1 - (len(anios) * 110)
for indice, anio in enumerate(anios):
    x = leyenda_x + indice * 110
    color = colores.get(anio, "#7A5195")
    dibujo.line((x, 83, x + 34, 83), fill=color, width=6)
    dibujo.text((x + 43, 83), str(anio), fill="#333333", font=fuente_regular, anchor="lm")

nota = (
    "Fuente: Intendencia de Montevideo. Los años incompletos se muestran "
    "solo para los meses con registros disponibles."
)
dibujo.text((margen_izq, alto - 55), nota, fill="#666666", font=fuente_regular)

imagen.save(salida, quality=95)
print(f"\nGráfico guardado correctamente en:\n{salida}")

# Abrir el gráfico con el visor de imágenes predeterminado del sistema.
# Si se ejecuta en un entorno sin interfaz gráfica, el PNG igualmente queda guardado.
try:
    imagen.show(title="Residuos mensuales")
except Exception as error:
    print(f"No se pudo abrir el visor de imágenes: {error}")

