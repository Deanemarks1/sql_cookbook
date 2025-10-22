import mysql.connector
import pandas as pd
import re

print("✅ Deane’s MySQL Connector V34 — Flask-safe + persists DB across USE calls + no default DB required test to try auto connect")



# Global state
CURRENT_DB = None
GLOBAL_SQL_CONFIG = None


def set_global_config(config):
    """Set connection defaults. Database is optional."""
    global GLOBAL_SQL_CONFIG, CURRENT_DB
    GLOBAL_SQL_CONFIG = config
    CURRENT_DB = config.get("database")  # may be None


class mysqlconnector:
    def __init__(self, query, host, user, password, database=None):
        global CURRENT_DB

        self.df = pd.DataFrame()
        self.result = []
        self.columns = []

        # Remove /* */ block comments and # inline comments
        cleaned_query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        cleaned_query = "\n".join(
            line for line in cleaned_query.splitlines()
            if not line.strip().startswith("#")
        )

        self.query = cleaned_query.strip()
        statements = [s.strip() for s in self.query.split(';') if s.strip()]

        # Start with last known DB or default; both may be None (allowed)
        current_db = CURRENT_DB or database

        for i, stmt in enumerate(statements):
            # Manually handle: USE dbname;   (supports backticks and $/_/-)
            use_match = re.match(r'(?i)^USE\s+`?([A-Za-z0-9_\-$]+)`?$', stmt)
            if use_match:
                current_db = use_match.group(1)
                CURRENT_DB = current_db
                print(f"📦 Switched default DB to: {CURRENT_DB}")
                continue  # Don't pass USE to SQL engine

            is_last = (i == len(statements) - 1)

            # ✅ Allow connecting without a database (needed for CREATE DATABASE, etc.)
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=current_db or None
            )
            cursor = conn.cursor(buffered=True)

            try:
                cursor.execute(stmt)

                if is_last and cursor.description:
                    self.columns = [col[0] for col in cursor.description]
                    self.result = [dict(zip(self.columns, row)) for row in cursor.fetchall()]
                    self.df = pd.DataFrame(self.result)

                    # Fix float → int if all values are whole numbers
                    for col in self.df.columns:
                        if pd.api.types.is_float_dtype(self.df[col]):
                            series = self.df[col]
                            if (series.dropna() % 1 == 0).all():
                                self.df[col] = series.astype("Int64")

                    self.df = self.df.convert_dtypes()
                    print("✅ Final SELECT returned rows.")
                else:
                    conn.commit()

            except Exception as e:
                print(f"❌ SQL Error in statement {i+1}: {e}")
                self.df = pd.DataFrame()

            finally:
                try:
                    cursor.close()
                    conn.close()
                except:
                    pass

    def to_df(self):
        return self.df

    def to_dict(self):
        return self.df.to_dict(orient='records')

    def to_json(self):
        return self.df.to_json(orient='records')

    def to_jinja(self):
        df_clean = self.df.copy()
        for col in df_clean.columns:
            if pd.api.types.is_timedelta64_dtype(df_clean[col]) or pd.api.types.is_datetime64_any_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].astype(str)
            elif pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].apply(lambda x: float(x) if pd.notnull(x) else None)
        return df_clean.to_dict(orient='records')

    def head(self, n=5):
        return self.df.head(n)

    def __repr__(self):
        return repr(self.df)

    def __str__(self):
        return str(self.df)

    def __getattr__(self, name):
        return getattr(self.df, name)


# 🔥 Simple wrapper: just run SQL
def run_sql(query):
    global GLOBAL_SQL_CONFIG
    if GLOBAL_SQL_CONFIG is None:
        raise Exception("❌ SQL_CONFIG not set. Call set_global_config(SQL_CONFIG) first.")

    return mysqlconnector(
        query,
        host=GLOBAL_SQL_CONFIG["host"],
        user=GLOBAL_SQL_CONFIG["user"],
        password=GLOBAL_SQL_CONFIG["password"],
        database=GLOBAL_SQL_CONFIG.get("database")  # can be None
    )












#SQL_Cookbook Connection Setup -- OCT 18 2025
#---------------------------------------------------------------------------------------##
import os
import sys

#base_dir = os.getcwd()
base_dir = os.getcwd() +'/'

# Add project paths
sys.path.append('/home/comradmarx/python_cook_book/')
sys.path.append('/Users/deanemarks/Desktop/python_cook_book')


# ✅ Define SQL config based on environment (NO default database here)
if 'deanemarks' in base_dir:
    SQL_CONFIG = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "Podcast20!!"
        # no "database" key
    }


elif 'comradmarx' in base_dir:
    SQL_CONFIG = {
        "host": "comradmarx.mysql.pythonanywhere-services.com",  # 👈 placeholder
        "user": "comradmarx",
        "password": "Podcast20!!"
        # no "database" key
    }

else:
    raise Exception("❌ Unknown environment — SQL_CONFIG not defined.")





# 🔧 Apply the config once
set_global_config(SQL_CONFIG)
#---------------------------------------------------------------------------------------##















