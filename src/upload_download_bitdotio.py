from sqlalchemy import create_engine
import csv
from io import StringIO
import pandas as pd

def psql_insert_copy(table, conn, keys, data_iter):
    """
    Execute SQL statement inserting data

    Parameters
    ----------
    table : pandas.io.sql.SQLTable
    conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys : list of str
        Column names
    data_iter : Iterable that iterates the values to be inserted
    """
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join(f'"{k}"' for k in keys)
        table_name = f'"{table.schema}"."{table.name}"'
        sql = f'COPY {table_name} ({columns}) FROM STDIN WITH CSV'
        cur.copy_expert(sql=sql, file=s_buf)


def upload_table(df, upload_schema, upload_table, bitio_pg_string):
    engine = create_engine(bitio_pg_string)

    with engine.connect() as conn:
        # truncate table if exists
        if engine.dialect.has_table(
            connection=conn, table_name=upload_table, schema=upload_schema
        ):
            conn.execute(f'TRUNCATE TABLE "{upload_schema}"."{upload_table}"')
        df.to_sql(
            upload_table,
            conn,
            schema=upload_schema,
            if_exists="append",
            index=False,
            method=psql_insert_copy,
        )

def download_dataset(target, pg_string):
    engine = create_engine(pg_string)
    # SQL for querying an entire table
    sql = f"""
        SELECT *
        FROM {target};
    """
    # Return SQL query as a pandas dataframe
    with engine.connect() as conn:
        # Set 1 minute statement timeout (units are milliseconds)
        conn.execute("SET statement_timeout = 60000;")
        df = pd.read_sql(sql, conn)
    return df