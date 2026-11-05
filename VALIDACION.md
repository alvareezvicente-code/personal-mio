# Comprobaciones del 05/11/2026

Entorno: Python 3.12 y versiones de `requirements.txt`. Comprobaciones ejecutadas por Codex; la revisión independiente del estudiante sigue pendiente.

## Ejecutado

- Clases 3, 5, 7, 10, 12 y 14 completas, desde un directorio temporal ajeno al repositorio. Todas finalizaron sin errores tras las correcciones documentadas.
- Tres pruebas de utilidades: detectar simultáneamente varias restricciones incumplidas; preservar huecos en una ventana temporal; rechazar una unión que duplica claves y conservar la fila sin pareja.
- Validador del ticket: un ejemplo sintético correcto y cuatro ejemplos inválidos (suma incorrecta, monto vacío, columnas incorrectas y monto no finito). No son una transcripción real del ticket.
- Clase 11 en modo preparación, sin solicitud a Gemini ni uso de claves.
- Once gráficos generados y revisados visualmente.

## Contrastes y decisiones

- Clase 3: doce respuestas contrastadas con la clave publicada en el material docente. El práctico comprueba tipos, seis casos de rigidez superior a blando, tres fallos introducidos, persistencia parquet y 40 transacciones con tres sucursales.
- Clase 12: conteos de faltantes, máximo nocturno de PM2.5 y aumento pequeño de R² contrastados con las soluciones docentes de los ejercicios 1-4. Se eligió otro criterio explícito para tránsito alto: superar la mediana del perfil horario (8 a 19). La solución del docente propone 8 a 17 y admite otras respuestas; ambos criterios son exploratorios.
- Clase 14: tablas y cardinalidades calculadas en pandas y comprobadas mediante aserciones, incluyendo la pérdida de 680 vuelos y el resultado de 22.525 en la unión interna de aviones.
- Clase 10: el modelo simple describe asociación pero rinde peor que predecir la media de entrenamiento en el corte cronológico usado. No se presenta como pronóstico validado ni efecto causal.

## Pendientes reales

Revisión y explicación del estudiante, desafío de equipo y experiencias personales anteriores. Clase 11 requiere modelo disponible, clave propia y cotejo manual del ticket. Clase 10 toma como insumo la tabla preparada y no reproduce la asignación espacial de detectores.

Para volver a comprobar los scripts, después de descargar los datos: `python verificar.py`.

Fuentes de contraste: [fundamentos](https://github.com/DavytJ/Introduccion-a-la-ciencia-de-datos/blob/71cbebe1b3cd96d58b4bc9789fd016c7ac874cbd/clases/clase3/clase03_fundamentos.qmd), [soluciones de clase 12](https://github.com/DavytJ/Introduccion-a-la-ciencia-de-datos/blob/71cbebe1b3cd96d58b4bc9789fd016c7ac874cbd/clases/clase13/clase12_soluciones(1).py), [consigna de uniones](https://github.com/DavytJ/Introduccion-a-la-ciencia-de-datos/blob/71cbebe1b3cd96d58b4bc9789fd016c7ac874cbd/clases/clase14/ejercicios_58_61_papel.pdf).
