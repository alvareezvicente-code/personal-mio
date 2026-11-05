# Resultados de clase 3

Ejercicios 1-4: tipos declarados; seis objetos por encima de blando; validación correcta sin problemas y copia rota con tres problemas. Diccionario de 6 x 6. CSV pierde categorías; parquet conserva rigidez ordenada.

Ejercicio 5, error real del intento sin configuración:

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xed in position 10: invalid continuation byte
```

El separador es punto y coma, el decimal es coma y la codificación latin1. Omitir decimal no detiene el programa: deja el peso como texto.

Ejercicio 6: la ruta parte de __file__. Una ruta con el nombre de usuario de otra persona no describe la estructura compartida.

Ejercicio 7: media ingenua 48.4500 g; media declarada 85.3125 g. Pandas reconoce NA y vacío; hay que declarar -99 y s/d. Es un problema de representación de una medición ausente que contamina el cálculo.

Ejercicio 8: monto medio ingenuo 169.2785; correcto 1471.5000 UYU. Hay 40 transacciones, fechas con día primero y tres sucursales tras quitar espacios. Son propiedades del archivo; no prueban cómo se recolectó. Pregunta al productor: ¿cada fila representa una venta final, e incluye devoluciones e impuestos?

Un cero de aristas es una medición si se constató que el objeto no tiene aristas. Si no se pudieron contar, corresponde un faltante. El diccionario debe precisar ambas convenciones en instrumento y faltante.

Desafío de equipo: pendiente de confirmar el tema y la unidad de observación del equipo; no se inventó una entrega grupal.
