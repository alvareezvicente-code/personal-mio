"""Ozono: inspección, agregación mensual y máximo diario de media móvil 8h.
Referencia: carga_y_transformacion.py de clase 7; solución independiente.
Se exige 75% de minutos para una hora, y ocho horas completas por ventana.
Es un criterio analítico explícito, no una certificación normativa.
"""
from pathlib import Path
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RAIZ))
from funciones.utilidades import media_movil_horaria

def main():
    salida = RAIZ/'salidas'/'clase07'
    graficos = RAIZ/'graficos'
    salida.mkdir(parents=True,exist_ok=True)
    graficos.mkdir(exist_ok=True)
    df = pd.read_csv(RAIZ/'data'/'o3_01_2024_04_2024.csv',encoding='utf-8-sig')
    df['fecha'] = pd.to_datetime(df['fecha'], errors='raise')
    df['estacion'] = df['estacion'].str.strip()
    df['o3'] = pd.to_numeric(df['o3'],errors='coerce')
    originales, repetidas = len(df), df.duplicated().sum()
    df = df.drop_duplicates()
    df['o3'] = df['o3'].where(df['o3'] >= 0)
    # Primero una medición por estación y minuto; así duplicados no inflan cobertura.
    minuto = df.groupby(['estacion',pd.Grouper(key='fecha',freq='min')])['o3'].mean()
    mensual = df.assign(mes=df['fecha'].dt.to_period('M').astype(str)).groupby(['estacion','mes'])['o3'].agg(['mean','count'])
    mensual.to_csv(salida/'mensual.csv')
    todas = []
    fig, ax = plt.subplots(figsize=(11,5))
    for estacion in df['estacion'].unique():
        serie = minuto.loc[estacion].sort_index()
        horario = serie.resample('h').agg(['mean','count'])
        horario['o3'] = horario['mean'].where(horario['count'] >= 45)
        horario['media_8h'] = media_movil_horaria(horario['o3'])
        diario = horario['media_8h'].resample('D').agg(['max','count'])
        # Día válido si al menos 18 ventanas completas terminan ese día.
        diario['max_8h_valido'] = diario['max'].where(diario['count'] >= 18)
        diario['estacion'] = estacion
        todas.append(diario)
        ax.plot(diario.index, diario['max_8h_valido'],label=estacion,linewidth=1)
    diario = pd.concat(todas)
    diario.to_csv(salida/'maximo_diario_8h.csv')
    ax.set(title='Ozono: máximo diario de la media móvil de 8 horas',xlabel='Fecha (2024)',ylabel='O3 (µg/m³)')
    ax.legend(); ax.grid(alpha=.2); fig.tight_layout()
    fig.savefig(graficos/'clase07_ozono_8h.png',dpi=150); plt.close(fig)
    fig,ax = plt.subplots(figsize=(9,4))
    for estacion, parte in mensual.groupby(level=0):
        p = parte.reset_index()
        ax.plot(p['mes'],p['mean'],marker='o',label=estacion)
    ax.set(title='Concentración mensual observada de ozono',xlabel='Mes',ylabel='O3 medio (µg/m³)')
    ax.legend(); fig.tight_layout(); fig.savefig(graficos/'clase07_ozono_mensual.png',dpi=150); plt.close(fig)
    resumen = diario.groupby('estacion')['max_8h_valido'].agg(['count','mean','max'])
    texto = f'''# Clase 7: resultados

Archivo: {originales} filas; {repetidas} duplicados exactos. Período observado: {df['fecha'].min()} a {df['fecha'].max()}.

Se leyó UTF-8 para conservar los nombres de estación. Se agregaron mediciones por minuto y hora, conservando los huecos. Una hora requiere 45 minutos válidos y una ventana requiere ocho horas válidas. Para informar un máximo diario se exigen 18 ventanas completas terminadas ese día.

Resumen por estación (días válidos, media y máximo de máximos diarios):

```text
{resumen.to_string()}
```

El promedio mensual resume niveles observados y el máximo de ocho horas describe episodios sostenidos; no contestan la misma pregunta. No se interpolaron huecos. Los criterios estrictos pueden excluir días y cambiar la comparación. El día se asigna al final de la ventana; no se infirió una zona horaria que la fuente no declara.
'''
    (salida/'resultados.md').write_text(texto,encoding='utf-8')
    print(texto)

if __name__ == '__main__':
    main()
