import csv
from pathlib import Path
from sqlalchemy import text
from book_manager.database.connection import ConexionDB

# (archivo_csv, nombre_tabla, mapeo_columnas)
TABLAS = [
    ("moneda.csv", "monedas", {"id_moneda": "id"}),
    ("tipo_cotizacion.csv", "tipos_cotizacion", {"id_tipo_cotizacion": "id"}),
    ("generos.csv", "generos", {"id_genero": "id"}),
    ("editorial.csv", "editoriales", {"id_editorial": "id"}),
    ("Precio.csv", "precios", {"id_precio": "id", "id_moneda": "moneda_id", "id_tipo_cotizacion": "tipo_cotizacion_id"}),
    ("cotizacion_dolar.csv", "cotizaciones_dolar", {"id_cotizacion": "id", "moneda": "moneda_id", "tipo_cotizacion": "tipo_cotizacion_id"}),
    ("libros.csv", "libros", {"id_libro": "id", "genero": "genero_id", "editorial": "editorial_id", "precio": "precio_id"}),
    ("stock.csv", "stocks", {"id_stock": "id", "libro": "libro_id"}),
]


def migrar_datos(carpeta_csvs: str, carpeta_sqls: str) -> None:
    """Lectura de CSV, creación de archivos sql y carga de datos a la BD"""
    ruta_csvs, ruta_sqls = Path(carpeta_csvs), Path(carpeta_sqls)
    ruta_sqls.mkdir(parents=True, exist_ok=True)
    db = ConexionDB()

    with db.transaccion() as sesion:
        for archivo, tabla, mapeo in TABLAS:
            ruta_csv = ruta_csvs / archivo
            if not ruta_csv.exists():
                continue

            sentencias = []
            with open(ruta_csv, mode="r", encoding="utf-8") as f:
                for fila in csv.DictReader(f):
                    cols, vals = [], []
                    for col, val in fila.items():
                        if not col or not col.strip():
                            continue
                        c = mapeo.get(col.strip(), col.strip())
                        v = (val or "").strip()

                        # Ajustes de formato (fechas y guion en stock)
                        if c == "fecha":
                            v = v.replace("/", "-")
                        elif c == "cantidad" and v == "-":
                            v = "0"

                        cols.append(c)
                        v_sql = v.replace("'", "''")
                        vals.append(f"'{v_sql}'")

                    sentencias.append(f"INSERT INTO {tabla} ({', '.join(cols)}) VALUES ({', '.join(vals)});\n")

            # 1. Guardar archivo .sql
            (ruta_sqls / f"{tabla}.sql").write_text("".join(sentencias), encoding="utf-8")

            # 2. Insertar en la BD si la tabla no tiene registros
            conteo = sesion.execute(text(f"SELECT COUNT(*) FROM {tabla}")).scalar()
            if conteo == 0:
                for s in sentencias:
                    sesion.execute(text(s))
                print(f"[Migrado] {tabla}: {len(sentencias)} registros.")
            else:
                print(f"[Omitido] {tabla}: ya tiene {conteo} registros.")

    db.cerrar_conexion()
    print("\n¡Migración finalizada con éxito!")
