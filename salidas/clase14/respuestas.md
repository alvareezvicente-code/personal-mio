# Clase 14: unir tablas

## 58
Left conserva cinco vuelos. Los nombres son United, American, JetBlue, United y faltante para DL. Inner conserva cuatro: se pierde el vuelo 5 porque DL no está en la tabla de aerolíneas.

## 59
La clave es dest en vuelos y faa en aeropuertos. Los destinos son George Bush Intercontinental, Miami Intl, faltante para SJU, Chicago Ohare Intl y Hartsfield Jackson Atlanta Intl. Inner conserva cuatro vuelos. Para evitar dos columnas name se eligieron aerolinea y aeropuerto_destino.

## 60
Con origin y hour quedan tres filas y las visibilidades son 10, 2 y 10. Solo con origin quedan seis filas:

```text
 vuelo origin  hour_vuelo  hour_clima  visib
     1    EWR           5           5   10.0
     1    EWR           5           6    2.0
     2    EWR           6           5   10.0
     2    EWR           6           6    2.0
     3    JFK           5           5   10.0
     3    JFK           5           6    0.5
```

Cada vuelo encuentra dos horarios del aeropuerto, incluso uno que no corresponde. Para conocer la visibilidad de salida hace falta la clave completa. Si falta JFK a las 5, left conserva tres vuelos (visib faltante en vuelo 3) e inner conserva dos.

## 61
A: igual (27.004); B: menos (26.324); C: más (646.428); D: igual (27.004).

B pierde 680 vuelos. En C cada vuelo aparece 23.938231 veces en promedio: falta hour en la clave, que une todas las horas del mismo aeropuerto y día.

D conserva 27.004 filas si es left aunque falte avión para 4.479 vuelos. Con inner quedan 22.525. Para estudiar antigüedad conviene conservar primero todos con left, medir la ausencia de año y explicitar sobre qué submuestra se calcula. Inner simplifica el cálculo, pero excluye vuelos y puede sesgar la composición. Mantener filas no recupera la antigüedad ausente.
