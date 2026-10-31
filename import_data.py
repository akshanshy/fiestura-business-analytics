import pandas as pd
import mysql.connector
from getpass import getpass

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=getpass("MySQL password:"),
    database="fiestura_analytics"
)

cursor = conn.cursor()

files = {
    "staging_events": "data/events_clean.csv",
    "staging_registrations": "data/registrations_clean.csv",
    "staging_payments": "data/payments_clean.csv"
}

columns = {
    "staging_events": [
        "event_id", "title", "category", "start_date",
        "end_date", "price", "capacity",
        "registered_count", "location", "created_at"
    ],

    "staging_registrations": [
        "registration_id", "user_id", "event_id", "created_at"
    ],

    "staging_payments": [
        "payment_id", "user_id", "event_id",
        "amount", "currency", "created_at"
    ]
}

try:
    for table, path in files.items():

        print(f"\nProcessing {table}...")

        df = pd.read_csv(path)

        col_names = columns[table]

        # Check required columns
        missing = set(col_names) - set(df.columns)

        if missing:
            raise ValueError(f"Missing columns in {path}: {missing}")

        # Convert dates
        date_columns = [
            col for col in df.columns
            if col.endswith("_date") or col == "created_at"
        ]

        for col in date_columns:
            parsed = pd.to_datetime(
                df[col],
                errors="coerce",
                utc=True
            )

            df[col] = parsed.apply(
                lambda x: x.strftime("%Y-%m-%d %H:%M:%S")
                if pd.notna(x) else None
            )

        # Convert missing values to SQL NULL
        df = df.astype(object).where(pd.notna(df), None)

        placeholders = ", ".join(["%s"] * len(col_names))

        query = f"""
            INSERT INTO {table} ({", ".join(col_names)})
            VALUES ({placeholders})
        """

        values = [
            tuple(row)
            for row in df[col_names].itertuples(
                index=False,
                name=None
            )
        ]

        cursor.executemany(query, values)
        conn.commit()

        print(f"{table}: {cursor.rowcount} rows imported")

    print("\nALL DATA IMPORTED SUCCESSFULLY!")

except Exception:
    conn.rollback()
    raise

finally:
    cursor.close()
    conn.close()