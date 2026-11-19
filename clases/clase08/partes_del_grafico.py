"""Clase 8: gráfico inicial, capas geométricas y versión corregida.

Se calculan las medias desde los datos originales de ozono. No modifica clase 7.
Referencia docente: clase8/vizualizacion_basica_python.py.
Solución nueva con asistencia de IA, 19/11/2026.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parents[2]

def guardar(fig, nombre):
    fig.savefig(RAIZ/'graficos'/nombre, dpi=150)
    plt.close(fig)

def main():
    salida = RAIZ/'salidas'/'clase08'
    salida.mkdir(parents=True, exist_ok=True)
    (RAIZ/'graficos').mkdir(exist_ok=True)
    ruta = RAIZ/'data'/'o3_01_2024_04_2024.csv'
    if not ruta.exists():
        raise FileNotFoundError(f'Falta {ruta}; ejecutar python datos/obtener_datos.py')
    original = pd.read_csv(ruta, encoding='utf-8-sig', parse_dates=['fecha'])
    original['o3'] = pd.to_numeric(original['o3'], errors='coerce')
    validos = original.dropna(subset=['fecha','o3']).copy()
    # La actividad usa las medias de todas las mediciones disponibles, como el ejemplo.
    validos['mes'] = validos['fecha'].dt.to_period('M').astype(str)
    mensual = validos.groupby('mes')['o3'].agg(media='mean', n_registros='size').reset_index()
    if mensual.empty:
        raise ValueError('No hay mediciones válidas para graficar')
    assert mensual.n_registros.sum() == len(validos)
    assert np.isclose(np.average(mensual.media, weights=mensual.n_registros), validos.o3.mean())
    mensual.to_csv(salida/'ozono_mensual.csv', index=False)
    x = np.arange(1,len(mensual)+1)
    y = mensual.media.to_numpy()

    # Reproducir problemas de comunicación para poder contrastar el antes y después.
    fig,ax = plt.subplots(figsize=(9,5))
    ax.plot(x,y,color='blue',linewidth=2)
    ax.scatter(x,y,color='red',s=50,zorder=3)
    ax.set(title='Concentración de Ozono en el ambiente, por mes, 2024',xlabel='Fecha',ylabel='Valores')
    ax.grid(alpha=.3)
    fig.tight_layout()
    guardar(fig,'clase08_partida.png')

    fig,axes = plt.subplots(1,2,figsize=(11,4))
    axes[0].plot(x,y,color='#2678a5',linewidth=2)
    axes[1].scatter(x,y,color='#2678a5',s=50)
    for ax,titulo in zip(axes,['Capa de línea: conecta las medias','Capa de puntos: muestra cada media']):
        ax.set(title=titulo,xlabel='Mes (2024)',ylabel='Ozono medio (µg/m³)')
        ax.set_xticks(x, mensual.mes)
        ax.grid(axis='y',alpha=.2)
    fig.tight_layout()
    guardar(fig,'clase08_geometria.png')

    nombres = {1:'Enero',2:'Febrero',3:'Marzo',4:'Abril',5:'Mayo',6:'Junio',
               7:'Julio',8:'Agosto',9:'Septiembre',10:'Octubre',11:'Noviembre',12:'Diciembre'}
    etiquetas = [f'{nombres[int(m[-2:])]}\n{m[:4]}' for m in mensual.mes]
    fig,ax = plt.subplots(figsize=(10,6))
    ax.plot(x,y,color='#2678a5',linewidth=2,marker='o',markersize=7)
    for posicion,valor in zip(x,y):
        ax.annotate(f'{valor:.1f}',(posicion,valor),xytext=(0,10),textcoords='offset points',ha='center')
    ax.set_xticks(x,etiquetas)
    ax.set_ylim(min(0,float(y.min())*1.2), max(5,float(y.max())*1.25))
    ax.set(title='Ozono en Montevideo: media de los registros por mes',xlabel='Mes',ylabel='Ozono, O3 (µg/m³)')
    ax.grid(axis='y',alpha=.25)
    ax.spines[['top','right']].set_visible(False)
    fig.text(.03,.04,'Fuente: Intendencia de Montevideo. Registros disponibles de Colón y Curva de Maroñas.',fontsize=9,color='#555555')
    fig.text(.03,.012,'Media ponderada por cantidad de registros; abril llega al 29/04. La cobertura difiere entre estaciones.',fontsize=9,color='#555555')
    fig.tight_layout(rect=(0,.095,1,1))
    guardar(fig,'clase08_corregida.png')
    texto = f'''# Clase 8: las partes de un gráfico

Resolución nueva preparada con asistencia de IA el 19/11/2026. Se compara una figura inicial con una corregida y se muestran por separado las capas de línea y puntos.

## Datos usados

Se leyeron {len(original):,} registros de ozono y se usaron {len(validos):,} con fecha y medición disponibles. Período: {validos.fecha.min()} a {validos.fecha.max()}.

```text
{mensual.to_string(index=False)}
```

Se promediaron todos los registros disponibles de las estaciones por mes. Eso pondera más a la estación que aporta más mediciones: no es el promedio con igual peso de las dos medias de estación. Los valores se calculan desde el CSV; no se copiaron de una imagen. No se interpolaron faltantes.

## Qué cambia y por qué

| Elemento | Figura inicial | Figura corregida |
|---|---|---|
| Datos y transformación | La media no se explica | Se declara qué observaciones se promedian y la cobertura incompleta |
| Eje horizontal | Números con rótulo Fecha | Nombres de meses y año |
| Eje vertical | Valores sin unidad | O3 en µg/m³ |
| Geometría | Línea y puntos con colores distintos sin significado | Una misma serie con línea y marcadores del mismo color |
| Escala | Ajuste automático | Rango que incluye cero y todas las medias, con espacio para etiquetas |
| Contexto | Sin fuente | Fuente, estaciones y fin del período disponibles |

Los puntos representan medias mensuales; las líneas solo conectan meses y no muestran mediciones intermedias. La figura de geometría hace explícitas ambas capas. Incluir cero es una decisión de comunicación para esta comparación, no una obligación universal para los gráficos de líneas.

## Límite de la afirmación

Se describe la media de las mediciones registradas; no se estima una exposición representativa de toda la ciudad ni se demuestra que los cambios sean causados por el tránsito. Una mejor presentación no corrige la desigual cobertura de los sensores.

Referencia: [ejemplo docente de visualización](https://github.com/DavytJ/Introduccion-a-la-ciencia-de-datos/blob/e17cf90d892bd5f0585aa2660f12b29e17e3c44a/clases/clase8/vizualizacion_basica_python.py). El ejemplo usa valores leídos de un gráfico; esta resolución recalcula las medias desde la fuente.
'''
    (salida/'resultados.md').write_text(texto,encoding='utf-8')
    print(texto)

if __name__ == '__main__':
    main()