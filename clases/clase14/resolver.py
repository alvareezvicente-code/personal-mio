"""Ejercicios 58-61: resultados exactos y pruebas de cardinalidad.
Fuente: ejercicios_58_61_papel.pdf del docente, clase 14.
"""
from pathlib import Path
import pandas as pd
RAIZ=Path(__file__).resolve().parents[2]

def main():
    salida=RAIZ/'salidas'/'clase14'; salida.mkdir(parents=True,exist_ok=True)
    vuelos=pd.DataFrame({'vuelo':[1,2,3,4,5],'carrier':['UA','AA','B6','UA','DL'],
        'dest':['IAH','MIA','SJU','ORD','ATL'],'dep_delay':[2,-4,33,0,-6]})
    aerolineas=pd.DataFrame({'carrier':['UA','AA','B6'],'aerolinea':['United Air Lines Inc.','American Airlines Inc.','JetBlue Airways']})
    e58=vuelos.merge(aerolineas,on='carrier',how='left',validate='many_to_one')
    assert e58.aerolinea.isna().tolist()==[False,False,False,False,True]
    assert len(vuelos.merge(aerolineas,on='carrier',how='inner'))==4
    e58.to_csv(salida/'ej58.csv',index=False)
    aeropuertos=pd.DataFrame({'faa':['IAH','MIA','ORD','ATL'],'aeropuerto_destino':['George Bush Intercontinental','Miami Intl','Chicago Ohare Intl','Hartsfield Jackson Atlanta Intl']})
    e59=vuelos.merge(aeropuertos,left_on='dest',right_on='faa',how='left',validate='many_to_one')
    assert e59.aeropuerto_destino.isna().tolist()==[False,False,True,False,False]
    assert len(vuelos.merge(aeropuertos,left_on='dest',right_on='faa',how='inner'))==4
    e59.to_csv(salida/'ej59.csv',index=False)
    v=pd.DataFrame({'vuelo':[1,2,3],'origin':['EWR','EWR','JFK'],'hour':[5,6,5]})
    clima=pd.DataFrame({'origin':['EWR','EWR','JFK','JFK'],'hour':[5,6,5,6],'visib':[10,2,10,.5]})
    correcto=v.merge(clima,on=['origin','hour'],how='left',validate='many_to_one')
    incompleto=v.merge(clima,on='origin',how='left',suffixes=('_vuelo','_clima'))
    assert len(correcto)==3 and correcto.visib.tolist()==[10,2,10]
    assert len(incompleto)==6
    incompleto.to_csv(salida/'ej60_clave_incompleta.csv',index=False)
    sin_jfk5=clima[~((clima.origin=='JFK')&(clima.hour==5))]
    assert len(v.merge(sin_jfk5,on=['origin','hour'],how='left'))==3
    assert len(v.merge(sin_jfk5,on=['origin','hour'],how='inner'))==2
    assert 27004-26324==680 and 27004-4479==22525
    texto=f'''# Clase 14: unir tablas

## 58
Left conserva cinco vuelos. Los nombres son United, American, JetBlue, United y faltante para DL. Inner conserva cuatro: se pierde el vuelo 5 porque DL no está en la tabla de aerolíneas.

## 59
La clave es dest en vuelos y faa en aeropuertos. Los destinos son George Bush Intercontinental, Miami Intl, faltante para SJU, Chicago Ohare Intl y Hartsfield Jackson Atlanta Intl. Inner conserva cuatro vuelos. Para evitar dos columnas name se eligieron aerolinea y aeropuerto_destino.

## 60
Con origin y hour quedan tres filas y las visibilidades son 10, 2 y 10. Solo con origin quedan seis filas:

```text
{incompleto.to_string(index=False)}
```

Cada vuelo encuentra dos horarios del aeropuerto, incluso uno que no corresponde. Para conocer la visibilidad de salida hace falta la clave completa. Si falta JFK a las 5, left conserva tres vuelos (visib faltante en vuelo 3) e inner conserva dos.

## 61
A: igual (27.004); B: menos (26.324); C: más (646.428); D: igual (27.004).

B pierde 680 vuelos. En C cada vuelo aparece {646428/27004:.6f} veces en promedio: falta hour en la clave, que une todas las horas del mismo aeropuerto y día.

D conserva 27.004 filas si es left aunque falte avión para 4.479 vuelos. Con inner quedan 22.525. Para estudiar antigüedad conviene conservar primero todos con left, medir la ausencia de año y explicitar sobre qué submuestra se calcula. Inner simplifica el cálculo, pero excluye vuelos y puede sesgar la composición. Mantener filas no recupera la antigüedad ausente.
'''
    (salida/'respuestas.md').write_text(texto,encoding='utf-8')
    print(texto)

if __name__=='__main__':
    main()
