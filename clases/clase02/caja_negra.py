"""Clase 2: remuestreo de filas y generación paramétrica de pesos.

Datos de ejemplo del docente, no mediciones personales del estudiante.
Fuente: DavytJ/Introduccion-a-la-ciencia-de-datos, clase2/generacion de datos.qmd.
Implementación nueva, 19/11/2026.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parents[2]

def main():
    salida = RAIZ/'salidas'/'clase02'
    graficos = RAIZ/'graficos'
    salida.mkdir(parents=True, exist_ok=True)
    graficos.mkdir(exist_ok=True)
    caja = pd.DataFrame({
        'objeto_id': range(1, 11),
        'textura': ['suave','rugoso','poroso','suave','rugoso','suave','poroso','rugoso','suave','poroso'],
        'rigidez': ['blando','rígido','medio','blando','rígido','rígido','blando','medio','medio','blando'],
        'num_aristas': [0,8,0,4,12,0,0,6,4,0],
        'peso_estimado_g': [45.,120.5,15.,85.,210.,35.,18.5,95.,70.,22.],
        'certeza_observador': [5,4,3,5,4,2,4,3,4,3],
    })
    caja['textura'] = caja['textura'].astype('category')
    caja['rigidez'] = pd.Categorical(caja['rigidez'], ['blando','medio','rígido'], ordered=True)
    caja['certeza_observador'] = pd.Categorical(caja['certeza_observador'], range(1,6), ordered=True)

    # Se remuestrean filas completas: no se rompen las relaciones entre columnas.
    bootstrap = caja.sample(n=100, replace=True, random_state=42).reset_index(drop=True)
    rng = np.random.default_rng(42)
    mu = caja['peso_estimado_g'].mean()
    sigma = caja['peso_estimado_g'].std(ddof=1)
    pesos_brutos = rng.normal(mu, sigma, size=500)
    pesos_recortados = np.clip(pesos_brutos, 1., None)
    sinteticos = pd.DataFrame({'peso_normal_g': pesos_brutos,
                               'peso_recortado_g': pesos_recortados,
                               'fue_recortado': pesos_brutos < 1})

    # Controles de procedencia y restricciones, además de verificar tamaños.
    assert len(bootstrap) == 100 and len(sinteticos) == 500
    assert bootstrap.merge(caja, on=list(caja.columns), how='inner').shape[0] == 100
    assert (pesos_recortados >= 1).all()
    assert np.array_equal(pesos_recortados[pesos_brutos >= 1], pesos_brutos[pesos_brutos >= 1])
    assert bootstrap['objeto_id'].duplicated().any()
    bootstrap.to_csv(salida/'bootstrap_100.csv', index=False)
    sinteticos.to_csv(salida/'pesos_sinteticos_500.csv', index=False)
    por_rigidez = pd.concat({
        'original': caja.groupby('rigidez', observed=True)['peso_estimado_g'].mean(),
        'bootstrap': bootstrap.groupby('rigidez', observed=True)['peso_estimado_g'].mean(),
    }, axis=1)
    por_rigidez.to_csv(salida/'peso_medio_por_rigidez.csv')

    # Mismos intervalos, sin ocultar la cola negativa ni los valores grandes.
    minimo = np.floor(min(0, pesos_brutos.min())/20)*20
    maximo = np.ceil(max(caja.peso_estimado_g.max(), pesos_brutos.max())/20)*20
    bins = np.arange(minimo, maximo+20, 20)
    fig, axes = plt.subplots(3, 1, figsize=(10,9), sharex=True)
    axes[0].hist(caja.peso_estimado_g, bins=bins, color='#2678a5')
    axes[0].set_title('Ejemplo docente: 10 objetos', loc='left')
    axes[1].hist(bootstrap.peso_estimado_g, bins=bins, color='#27895c')
    axes[1].set_title('Remuestreo con reemplazo: 100 filas', loc='left')
    axes[2].hist(pesos_brutos, bins=bins, histtype='step', linewidth=1.8, color='#945cac', label='Normal sin corregir')
    axes[2].hist(pesos_recortados, bins=bins, color='#de9a24', alpha=.55, label='Normal recortada a 1 g')
    axes[2].set_title('Generación paramétrica: 500 pesos', loc='left')
    axes[2].legend()
    for ax in axes:
        ax.set_ylabel('Cantidad de filas')
        ax.axvline(0, color='gray', linestyle=':', linewidth=.8)
        ax.grid(axis='y', alpha=.2)
    axes[-1].set_xlabel('Peso estimado (g)')
    fig.suptitle('Caja negra: repetir datos no equivale a medir nuevos objetos')
    fig.text(.02,.015,'Fuente: datos de ejemplo de clase 2. Semilla 42. Las escalas verticales difieren por tamaño de muestra.',fontsize=9)
    fig.tight_layout(rect=(0,.045,1,.97))
    fig.savefig(graficos/'clase02_caja_negra.png', dpi=150)
    plt.close(fig)
    texto = f'''# Clase 2: caja negra, bootstrap y datos sintéticos

Resolución preparada el 19/11/2026. Se usan diez registros del ejemplo docente, no observaciones personales nuevas.

## Resultados

- Peso original medio: {mu:.4f} g; desviación estándar muestral: {sigma:.4f} g.
- Remuestreo: 100 filas completas con reemplazo, procedentes de {bootstrap.objeto_id.nunique()} objetos distintos. Peso medio: {bootstrap.peso_estimado_g.mean():.4f} g.
- Normal ajustada: 500 pesos, de los cuales {(pesos_brutos <= 0).sum()} no son positivos y {(pesos_brutos < 1).sum()} quedan por debajo de 1 g.
- Al recortar a 1 g, la media pasa de {pesos_brutos.mean():.4f} a {pesos_recortados.mean():.4f} g. El recorte modifica la distribución y concentra observaciones en 1 g.

Medias por rigidez (g):

```text
{por_rigidez.to_string()}
```

## Interpretación

El bootstrap conserva filas observadas y sus combinaciones de variables, pero no agrega información independiente ni garantiza conservar exactamente las proporciones. Las 100 filas no son 100 objetos medidos. Este remuestreo ampliado es el ejercicio de clase; no es una distribución de réplicas del estimador ni un intervalo de confianza.

La normal inventa pesos bajo un supuesto paramétrico y puede producir pesos físicamente imposibles. Recortarlos evita valores no positivos, pero no demuestra que el modelo represente objetos reales. Solo se generó peso: no corresponde asignarle textura y rigidez sin un modelo conjunto.

La medición táctil y la certeza del observador pertenecen al proceso de generación del dato. Aumentar filas no corrige errores de medición, sesgos o falta de diversidad en los diez registros iniciales.

Fuente: [material de clase 2](https://github.com/DavytJ/Introduccion-a-la-ciencia-de-datos/blob/e17cf90d892bd5f0585aa2660f12b29e17e3c44a/clases/clase2/generacion%20de%20datos.qmd).
'''
    (salida/'resultados.md').write_text(texto, encoding='utf-8')
    print(texto)

if __name__ == '__main__':
    main()