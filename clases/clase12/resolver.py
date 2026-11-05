"""Siete ejercicios de tránsito y aire. Consigna: clase13/clase12_ejercicios(1).py
del repositorio docente. Solución nueva con asistencia de Codex.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RAIZ))
from funciones.utilidades import preparar_aire

def main():
    salida = RAIZ/'salidas'/'clase12'; salida.mkdir(parents=True,exist_ok=True)
    graficos = RAIZ/'graficos'; graficos.mkdir(exist_ok=True)
    datos = preparar_aire()
    columnas = ['transito','no2','pm25','franja','tipo_dia','transito_rel','log_pm25']
    faltantes = datos[columnas].isna().groupby(datos['estacion']).sum()
    faltantes.to_csv(salida/'ej1_faltantes.csv')
    mensajes = ['# Clase 12: respuestas y resultados',
        '## 1. Faltantes', faltantes.to_string(),
        'La transformación logarítmica conserva los faltantes de PM2.5 y excluye valores no positivos. Franja y tipo de día se construyen de la hora; tránsito relativo depende del tránsito original.']

    # 2: definición exploratoria explícita; se calcula sin mirar NO2.
    semana = datos[(datos['estacion']=='Tres Cruces') & (datos['tipo_dia']=='lunes a viernes')]
    por_hora = semana.groupby('h')['transito'].mean()
    umbral = por_hora.median()
    horas_altas = por_hora[por_hora > umbral].index.tolist()
    datos['transito_alto'] = datos['h'].isin(horas_altas)
    originales = {7,8,9,17,18,19}
    por_hora.to_csv(salida/'ej2_por_hora.csv')
    fig,axes = plt.subplots(2,1,figsize=(10,7),sharex=True)
    for ax, titulo, horas in zip(axes,['Definición de la consigna','Horas por encima de la mediana del perfil diario'],[originales,set(horas_altas)]):
        ax.bar(por_hora.index,por_hora.values,color=['#1d7874' if h in horas else '#cbd5e1' for h in por_hora.index])
        ax.set(title=titulo,ylabel='Vehículos/hora')
    axes[-1].set(xlabel='Hora del día',xticks=range(24)); fig.tight_layout()
    fig.savefig(graficos/'clase12_ej2_horas.png',dpi=150); plt.close(fig)
    mensajes += ['## 2. Horas de tránsito alto',f'Criterio elegido: media de tránsito de la hora mayor que la mediana de las 24 medias ({umbral:.2f}). Horas: {horas_altas}.',
        f'Horas marcadas inicialmente que no cumplen este criterio: {sorted(originales-set(horas_altas))}. Horas omitidas por la definición inicial: {sorted(set(horas_altas)-originales)}.',
        'Es una definición exploratoria para Tres Cruces en días hábiles de este mes; no una regla universal.']

    # 3: paneles de PM2.5, sin línea de referencia en 1.
    por_franja = datos.groupby(['estacion','franja'],observed=True)[['transito_rel','pm25']].mean()
    por_franja.to_csv(salida/'ej3_franjas.csv')
    estaciones = sorted(datos['estacion'].unique())
    fig,axes = plt.subplots(1,len(estaciones),figsize=(13,4),sharey=True)
    maximos=[]
    for ax, estacion in zip(axes,estaciones):
        p = por_franja.loc[estacion]
        ax.bar(p.index.astype(str),p['pm25'],color='#c77748')
        ax.set_title(estacion); ax.tick_params(axis='x',rotation=25)
        maximos.append(f'{estacion}: PM2.5 máximo en {p.pm25.idxmax()}; tránsito relativo máximo en {p.transito_rel.idxmax()}.')
    axes[0].set_ylabel('PM2.5 medio (µg/m³)'); fig.tight_layout()
    fig.savefig(graficos/'clase12_ej3_pm25.png',dpi=150); plt.close(fig)
    mensajes += ['## 3. PM2.5 por franja',*maximos]

    # 4 y 5: misma muestra completa para comparar R².
    tc = datos[(datos['estacion']=='Tres Cruces') & datos['no2'].notna()].copy()
    completa = tc.dropna(subset=['no2','transito_miles','pm25','franja']).copy()
    completa['noche'] = (completa['franja']=='noche').astype(int)
    m3 = smf.ols('no2 ~ transito_miles + pm25',data=completa).fit()
    m4 = smf.ols('no2 ~ transito_miles + pm25 + C(franja)',data=completa).fit()
    m5 = smf.ols('no2 ~ transito_miles + pm25 + noche',data=completa).fit()
    mensajes += ['## 4. Agregar franja',f'Misma muestra: {len(completa)} horas. R² inicial {m3.rsquared:.6f}; con franja {m4.rsquared:.6f}; aumento {m4.rsquared-m3.rsquared:.6f}.',
        'El R² dentro de muestra no puede bajar al agregar regresores sobre las mismas filas. No demuestra mejora predictiva fuera de muestra.',
        '## 5. Indicador noche',f'Coeficiente de noche: {m5.params["noche"]:.6f} µg/m³, a igual tránsito y PM2.5. R²: {m5.rsquared:.6f}.']

    # 6: estimar las cuatro pendientes y elegir la mayor a partir del gráfico.
    pendientes={}
    fig,ax = plt.subplots(figsize=(9,5))
    colores = dict(zip(['madrugada','mañana','tarde','noche'],['#2678a5','#de9a24','#27895c','#945cac']))
    for franja, parte in tc.groupby('franja',observed=True):
        p=parte.dropna(subset=['transito_miles','no2'])
        modelo=smf.ols('no2 ~ transito_miles',data=p).fit()
        pendientes[str(franja)]=float(modelo.params['transito_miles'])
        ax.scatter(p.transito_miles,p.no2,s=12,alpha=.5,color=colores[str(franja)],label=str(franja))
        x=np.array([p.transito_miles.min(),p.transito_miles.max()])
        ax.plot(x,modelo.params['Intercept']+modelo.params['transito_miles']*x,color=colores[str(franja)])
    ax.set(title='Tránsito y NO2 por franja: Tres Cruces',xlabel='Miles de vehículos/hora',ylabel='NO2 (µg/m³)')
    ax.legend(); fig.tight_layout(); fig.savefig(graficos/'clase12_ej6_rectas.png',dpi=150); plt.close(fig)
    mayor=max(pendientes,key=pendientes.get)
    tc['franja_empinada']=(tc.franja==mayor).astype(int)
    m7=smf.ols('no2 ~ transito_miles * franja_empinada',data=tc).fit()
    mensajes += ['## 6. Interacción',f'Pendientes por franja: {pendientes}. La mayor es {mayor}.',
        f'R² con interacción binaria: {m7.rsquared:.6f}. El término de interacción mide cuánto cambia la pendiente respecto del resto de las horas.']

    # 7: separar los grupos de tarde por tipo de día.
    tarde=tc[tc.franja=='tarde'].copy()
    fig,ax=plt.subplots(figsize=(9,5))
    for tipo,p in tarde.groupby('tipo_dia'):
        ax.scatter(p.transito_miles,p.no2,s=22,alpha=.65,label=tipo)
        m=smf.ols('no2 ~ transito_miles',data=p).fit()
        x=np.array([p.transito_miles.min(),p.transito_miles.max()])
        ax.plot(x,m.params['Intercept']+m.params['transito_miles']*x)
    ax.set(title='Tarde: días hábiles y fin de semana',xlabel='Miles de vehículos/hora',ylabel='NO2 (µg/m³)')
    ax.legend(); fig.tight_layout(); fig.savefig(graficos/'clase12_ej7_tarde.png',dpi=150); plt.close(fig)
    grupos=tarde.groupby('tipo_dia')[['transito_miles','no2']].agg(['count','mean'])
    grupos.to_csv(salida/'ej7_grupos.csv')
    m8=smf.ols('no2 ~ transito_miles * C(tipo_dia)',data=tarde).fit()
    mensajes += ['## 7. Los grupos de la tarde',grupos.to_string(),
        'Los grupos se relacionan con días hábiles y fin de semana, que tienen niveles de tránsito distintos. La separación no implica dos causas de contaminación identificadas.',
        f'Modelo propuesto en la tarde: no2 ~ transito_miles * C(tipo_dia). R² {m8.rsquared:.6f}.',
        '## Límites comunes',
        'Las observaciones horarias están autocorrelacionadas. Los coeficientes y R² describen asociaciones; los p-valores ordinarios no justifican inferencia causal. Seleccionar la franja con los mismos datos es exploratorio.']
    for nombre,modelo in [('tc3',m3),('tc4',m4),('tc5',m5),('tc7',m7),('tarde',m8)]:
        pd.DataFrame({'coeficiente':modelo.params}).to_csv(salida/f'modelo_{nombre}.csv')
    assert np.isfinite(m4.rsquared) and m4.rsquared >= m3.rsquared-1e-10
    texto='\n\n'.join(mensajes)
    (salida/'resultados.md').write_text(texto,encoding='utf-8')
    print(texto)

if __name__ == '__main__':
    main()
