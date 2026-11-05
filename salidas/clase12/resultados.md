# Clase 12: respuestas y resultados

## 1. Faltantes

                   transito  no2  pm25  franja  tipo_dia  transito_rel  log_pm25
estacion                                                                        
Curva de Maronias         0   65     0       0         0             0         0
Museo Romántico           0  720   144       0         0             0       144
Tres Cruces               0  429   326       0         0             0       326

La transformación logarítmica conserva los faltantes de PM2.5 y excluye valores no positivos. Franja y tipo de día se construyen de la hora; tránsito relativo depende del tránsito original.

## 2. Horas de tránsito alto

Criterio elegido: media de tránsito de la hora mayor que la mediana de las 24 medias (30485.45). Horas: [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19].

Horas marcadas inicialmente que no cumplen este criterio: [7]. Horas omitidas por la definición inicial: [10, 11, 12, 13, 14, 15, 16].

Es una definición exploratoria para Tres Cruces en días hábiles de este mes; no una regla universal.

## 3. PM2.5 por franja

Curva de Maronias: PM2.5 máximo en noche; tránsito relativo máximo en tarde.

Museo Romántico: PM2.5 máximo en noche; tránsito relativo máximo en tarde.

Tres Cruces: PM2.5 máximo en noche; tránsito relativo máximo en tarde.

## 4. Agregar franja

Misma muestra: 291 horas. R² inicial 0.473137; con franja 0.486127; aumento 0.012990.

El R² dentro de muestra no puede bajar al agregar regresores sobre las mismas filas. No demuestra mejora predictiva fuera de muestra.

## 5. Indicador noche

Coeficiente de noche: 3.818586 µg/m³, a igual tránsito y PM2.5. R²: 0.481316.

## 6. Interacción

Pendientes por franja: {'madrugada': 2.9383803809734648, 'mañana': 0.5142862444670249, 'tarde': 0.8038132147092224, 'noche': 1.092899168248093}. La mayor es madrugada.

R² con interacción binaria: 0.397535. El término de interacción mide cuánto cambia la pendiente respecto del resto de las horas.

## 7. Los grupos de la tarde

                transito_miles              no2           
                         count       mean count       mean
tipo_dia                                                  
fin de semana               24  28.902708    24  41.790972
lunes a viernes             50  42.181460    50  49.992244

Los grupos se relacionan con días hábiles y fin de semana, que tienen niveles de tránsito distintos. La separación no implica dos causas de contaminación identificadas.

Modelo propuesto en la tarde: no2 ~ transito_miles * C(tipo_dia). R² 0.229264.

## Límites comunes

Las observaciones horarias están autocorrelacionadas. Los coeficientes y R² describen asociaciones; los p-valores ordinarios no justifican inferencia causal. Seleccionar la franja con los mismos datos es exploratorio.