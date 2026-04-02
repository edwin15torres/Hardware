
SELECT id_transaccion, date(fecha) AS fecha, detalle_transaccion, egreso, TRIM(SUBSTR(detalle_transaccion, INSTR(detalle_transaccion, ':') + 1)) AS nombre
FROM transacciones
WHERE detalle_transaccion LIKE '%NOMINA%';