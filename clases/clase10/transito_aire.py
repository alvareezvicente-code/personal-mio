"""Exploración propia sobre la tabla preparada por la cátedra.
No reconstruye el emparejamiento espacial de sensores desde los datos crudos.
Muestra ritmos diarios, correlaciones, rezagos y un modelo descriptivo.
"""
from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
RAIZ=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RAIZ))
from funciones.utilidades import preparar_aire

def guardar(fig,nombre):
    fig.tight_layout(); fig.savefig(RAIZ/'graficos'/f'clase10_{nombre}.png',dpi=150); plt.close(fig)

def main():
    salida=RAIZ/'salidas'/'clase10'; salida.mkdir(parents=True,exist_ok=True)
    (RAIZ/'graficos').mkdir(exist_ok=True)
    df=preparar_aire()
    df.groupby('estacion')[['transito','no2','pm25']].agg(['count','mean','std']).to_csv(salida/'resumen_estaciones.csv')
    correlaciones=[]
    fig,axes=plt.subplots(1,3,figsize=(14,4))
    for ax,(estacion,p) in zip(axes,df.groupby('estacion')):
        c=p[['transito','no2','pm25']].corr()
        correlaciones.append({'estacion':estacion,'transito_no2':c.loc['transito','no2'],
            'transito_pm25':c.loc['transito','pm25'],'no2_pm25':c.loc['no2','pm25']})
        ax.scatter(p.transito/1000,p.no2,s=9,alpha=.35)
        ax.set(title=estacion,xlabel='Miles de vehículos/hora')
        if not p.no2.notna().any():
            ax.text(.5,.5,'Sin mediciones de NO2',ha='center',va='center',transform=ax.transAxes)
            ax.set_xticks([]); ax.set_yticks([])
    axes[0].set_ylabel('NO2 (µg/m³)'); guardar(fig,'correlaciones')
    tabla_cor=pd.DataFrame(correlaciones); tabla_cor.to_csv(salida/'correlaciones.csv',index=False)
    tc=df[df.estacion=='Tres Cruces'].set_index('hora').asfreq('h')
    perfil=tc.groupby(tc.index.hour)[['transito','no2','pm25']].mean()
    fig,axes=plt.subplots(3,1,figsize=(10,8),sharex=True)
    for ax,col,etiqueta in zip(axes,['transito','no2','pm25'],['Vehículos/hora','NO2 (µg/m³)','PM2.5 (µg/m³)']):
        ax.plot(perfil.index,perfil[col],marker='o'); ax.set_ylabel(etiqueta)
    axes[0].set_title('Tres Cruces: perfil horario medio'); axes[-1].set_xlabel('Hora del día')
    guardar(fig,'perfil_diario')
    fig,axes=plt.subplots(2,1,figsize=(11,6),sharex=True)
    semana=tc.loc['2024-06-03':'2024-06-09']
    axes[0].plot(semana.index,semana.transito/1000); axes[0].set_ylabel('Miles vehículos/h')
    axes[1].plot(semana.index,semana.no2); axes[1].set_ylabel('NO2 (µg/m³)')
    axes[0].set_title('Tres Cruces: una semana, huecos conservados'); guardar(fig,'semana')
    sin_ciclo=tc[['transito','no2']]-tc.groupby(tc.index.hour)[['transito','no2']].transform('mean')
    r_cruda=tc[['transito','no2']].corr().iloc[0,1]
    r_sin=sin_ciclo.corr().iloc[0,1]
    lags=pd.DataFrame({'rezago_h':range(-24,25),
        'correlacion':[sin_ciclo.transito.shift(h).corr(sin_ciclo.no2) for h in range(-24,25)]})
    lags.to_csv(salida/'rezagos_sin_ciclo.csv',index=False)
    fig,ax=plt.subplots(figsize=(9,4)); ax.plot(lags.rezago_h,lags.correlacion,marker='.')
    ax.set(title='Correlaciones tras quitar el perfil horario',xlabel='Rezago del tránsito (h; positivo = tránsito anterior)',ylabel='Correlación con NO2')
    ax.axhline(0,color='gray',linewidth=.7); guardar(fig,'rezagos')
    muestra=tc.dropna(subset=['no2','transito_miles']).copy()
    modelo=smf.ols('no2 ~ transito_miles',data=muestra).fit()
    pd.DataFrame({'coeficiente':modelo.params}).to_csv(salida/'modelo_lineal.csv')
    residuo=pd.Series(np.nan,index=tc.index)
    residuo.loc[muestra.index]=modelo.resid
    ar1=residuo.corr(residuo.shift(1))
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    axes[0].scatter(muestra.transito_miles,muestra.no2,s=10,alpha=.4)
    x=np.linspace(muestra.transito_miles.min(),muestra.transito_miles.max(),100)
    axes[0].plot(x,modelo.params['Intercept']+modelo.params['transito_miles']*x,color='#c77748')
    axes[0].set(xlabel='Miles de vehículos/h',ylabel='NO2 (µg/m³)',title='Recta descriptiva')
    axes[1].scatter(modelo.fittedvalues,modelo.resid,s=10,alpha=.4)
    axes[1].axhline(0,color='gray'); axes[1].set(xlabel='NO2 predicho',ylabel='Residuo',title='Error del modelo')
    guardar(fig,'modelo_y_residuos')
    # Validación cronológica, sin mezclar futuro y pasado al azar.
    corte=muestra.index[int(len(muestra)*.7)]
    entrenamiento=muestra[muestra.index<corte]; prueba=muestra[muestra.index>=corte]
    extra='No hay observaciones suficientes en uno de los dos períodos para validar.'
    if len(entrenamiento)>3 and len(prueba)>0:
        temporal=smf.ols('no2 ~ transito_miles',data=entrenamiento).fit()
        rmse=np.sqrt(np.mean((prueba.no2-temporal.predict(prueba))**2))
        base=np.sqrt(np.mean((prueba.no2-entrenamiento.no2.mean())**2))
        comparacion='El modelo supera a la referencia en este corte.' if rmse<base else 'El modelo no mejora la referencia simple en este corte.'
        extra=f'Corte cronológico al 70% de las horas disponibles ({corte}). Entrenamiento: {len(entrenamiento)} horas; prueba: {len(prueba)}. RMSE modelo {rmse:.4f}; referencia de media de entrenamiento {base:.4f} µg/m³. {comparacion}'
    texto=f'''# Clase 10: tránsito y aire

Se utilizó la tabla horaria preparada por la cátedra (2.160 filas, tres estaciones). No se reconstruyó el emparejamiento geográfico original; ese resultado se toma como insumo y se atribuye al docente. Se conservaron las horas de la tabla, etiquetadas con Z/UTC, para reproducir las franjas de la consigna; no se reinterpretaron como hora local de Montevideo.

Correlaciones por pares completos:

```text
{tabla_cor.to_string(index=False)}
```

En Tres Cruces la correlación tránsito-NO2 es {r_cruda:.6f}; tras restar a cada variable su media por hora del día es {r_sin:.6f}. La diferencia indica cuánto de la asociación se relaciona con un ritmo diario compartido; no identifica un efecto causal.

Modelo con {int(modelo.nobs)} horas: NO2 = {modelo.params['Intercept']:.6f} + {modelo.params['transito_miles']:.6f} × miles de vehículos/hora. R² = {modelo.rsquared:.6f}. Correlación de residuos a una hora, sin saltar huecos: {ar1:.6f}.

{extra}

Una estación sin NO2 no permite estimar su correlación: NaN no significa cero. Las diferencias entre estaciones pueden reflejar cobertura y ubicación de los sensores. Los rezagos son exploratorios; buscar el máximo entre muchos no prueba causalidad. La autocorrelación invalida tratar las horas como observaciones independientes para inferencia ordinaria. Los promedios horarios usados para quitar ciclo se calculan sobre todo el mes con propósito descriptivo, y no se usan en la validación temporal.
'''
    (salida/'resultados.md').write_text(texto,encoding='utf-8'); print(texto)

if __name__=='__main__':
    main()
