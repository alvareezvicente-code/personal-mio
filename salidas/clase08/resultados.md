# Clase 8: las partes de un gráfico

Resolución nueva preparada con asistencia de IA el 19/11/2026. Se compara una figura inicial con una corregida y se muestran por separado las capas de línea y puntos.

## Datos usados

Se leyeron 291,926 registros de ozono y se usaron 255,767 con fecha y medición disponibles. Período: 2024-01-01 00:00:00 a 2024-04-29 23:59:00.

```text
    mes     media  n_registros
2024-01 29.108470        81700
2024-02 35.576710        42954
2024-03 23.997040        60466
2024-04 25.665676        70647
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