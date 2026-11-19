# Clase 2: caja negra, bootstrap y datos sintéticos

Resolución preparada con asistencia de IA el 19/11/2026. Se usan diez registros del ejemplo docente, no observaciones personales nuevas.

## Resultados

- Peso original medio: 71.6000 g; desviación estándar muestral: 60.3747 g.
- Remuestreo: 100 filas completas con reemplazo, procedentes de 10 objetos distintos. Peso medio: 74.4050 g.
- Normal ajustada: 500 pesos, de los cuales 57 no son positivos y 61 quedan por debajo de 1 g.
- Al recortar a 1 g, la media pasa de 70.8075 a 73.9068 g. El recorte modifica la distribución y concentra observaciones en 1 g.

Medias por rigidez (g):

```text
           original   bootstrap
rigidez                        
blando    42.625000   40.144737
medio     60.000000   66.666667
rígido   121.833333  135.192308
```

## Interpretación

El bootstrap conserva filas observadas y sus combinaciones de variables, pero no agrega información independiente ni garantiza conservar exactamente las proporciones. Las 100 filas no son 100 objetos medidos. Este remuestreo ampliado es el ejercicio de clase; no es una distribución de réplicas del estimador ni un intervalo de confianza.

La normal inventa pesos bajo un supuesto paramétrico y puede producir pesos físicamente imposibles. Recortarlos evita valores no positivos, pero no demuestra que el modelo represente objetos reales. Solo se generó peso: no corresponde asignarle textura y rigidez sin un modelo conjunto.

La medición táctil y la certeza del observador pertenecen al proceso de generación del dato. Aumentar filas no corrige errores de medición, sesgos o falta de diversidad en los diez registros iniciales.

Fuente: [material de clase 2](https://github.com/DavytJ/Introduccion-a-la-ciencia-de-datos/blob/e17cf90d892bd5f0585aa2660f12b29e17e3c44a/clases/clase2/generacion%20de%20datos.qmd).