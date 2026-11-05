# Clase 10: tránsito y aire

Se utilizó la tabla horaria preparada por la cátedra (2.160 filas, tres estaciones). No se reconstruyó el emparejamiento geográfico original; ese resultado se toma como insumo y se atribuye al docente. Se conservaron las horas de la tabla, etiquetadas con Z/UTC, para reproducir las franjas de la consigna; no se reinterpretaron como hora local de Montevideo.

Correlaciones por pares completos:

```text
         estacion  transito_no2  transito_pm25  no2_pm25
Curva de Maronias      0.146595      -0.152830  0.547996
  Museo Romántico           NaN      -0.098283       NaN
      Tres Cruces      0.587549      -0.024968  0.398913
```

En Tres Cruces la correlación tránsito-NO2 es 0.587549; tras restar a cada variable su media por hora del día es 0.367445. La diferencia indica cuánto de la asociación se relaciona con un ritmo diario compartido; no identifica un efecto causal.

Modelo con 291 horas: NO2 = 18.283903 + 0.793598 × miles de vehículos/hora. R² = 0.345214. Correlación de residuos a una hora, sin saltar huecos: 0.797179.

Corte cronológico al 70% de las horas disponibles (2024-06-13 18:00:00+00:00). Entrenamiento: 203 horas; prueba: 88. RMSE modelo 18.6777; referencia de media de entrenamiento 15.5214 µg/m³. El modelo no mejora la referencia simple en este corte.

Una estación sin NO2 no permite estimar su correlación: NaN no significa cero. Las diferencias entre estaciones pueden reflejar cobertura y ubicación de los sensores. Los rezagos son exploratorios; buscar el máximo entre muchos no prueba causalidad. La autocorrelación invalida tratar las horas como observaciones independientes para inferencia ordinaria. Los promedios horarios usados para quitar ciclo se calculan sobre todo el mes con propósito descriptivo, y no se usan en la validación temporal.
