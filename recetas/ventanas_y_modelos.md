# Ventanas temporales y comparación de modelos

Una media de ocho filas no representa ocho horas si faltan marcas de tiempo. Ordenar, resolver duplicados, reindexar por hora y exigir ocho observaciones válidas por ventana. Registrar también la cobertura diaria.

Para comparar modelos anidados, usar la misma muestra de filas completas. Un aumento del R² dentro de muestra es esperable al agregar variables: evaluar también una separación cronológica y una referencia simple. La correlación horaria y los rezagos no prueban causalidad.

En `transito_aire_junio2024.csv` el reloj lleva Z/UTC. Las franjas de estos ejercicios respetan el reloj de la consigna. Un análisis de horarios locales requiere revisar primero cómo se construyó esa fecha y qué zona corresponde.
