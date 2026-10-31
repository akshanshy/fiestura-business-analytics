import pandas as pd
from pathlib import Path

DATA = Path("data")

# 1. Clean Events
events = pd.read_csv(DATA / "fiestura.events.csv")

events = events.rename(columns={
    "_id": "event_id",
    "startDate": "start_date",
    "endDate": "end_date",
    "createdAt": "created_at",
    "registeredCount": "registered_count"
})

events = events[[
    "event_id", "title", "category", "start_date",
    "end_date", "price", "capacity",
    "registered_count", "location", "created_at"
]]

# 2. Clean Registrations
registrations = pd.read_csv(DATA / "fiestura.registrations.csv")

registrations = registrations.rename(columns={
    "_id": "registration_id",
    "userId": "user_id",
    "eventId": "event_id",
    "createdAt": "created_at"
})

registrations = registrations[[
    "registration_id", "user_id", "event_id", "created_at"
]]

# 3. Clean Payments
payments = pd.read_csv(DATA / "fiestura.payments.csv")

payments = payments.rename(columns={
    "_id": "payment_id",
    "userId": "user_id",
    "eventId": "event_id",
    "createdAt": "created_at"
})

payments = payments[[
    "payment_id",
    "user_id",
    "event_id",
    "amount",
    "currency",
    "created_at"
]]

# Standardize dates
for df, columns in [
    (events, ["start_date", "end_date", "created_at"]),
    (registrations, ["created_at"]),
    (payments, ["created_at"])
]:
    for col in columns:
        df[col] = pd.to_datetime(
            df[col], errors="coerce", utc=True
        ).dt.strftime("%Y-%m-%d %H:%M:%S")

# Remove rows without primary IDs
events = events.dropna(subset=["event_id"])
registrations = registrations.dropna(subset=["registration_id"])
payments = payments.dropna(subset=["payment_id"])

# Export
events.to_csv(DATA / "events_clean.csv", index=False)
registrations.to_csv(DATA / "registrations_clean.csv", index=False)
payments.to_csv(DATA / "payments_clean.csv", index=False)

print("CLEANING COMPLETE")
print("Events:", len(events))
print("Registrations:", len(registrations))
print("Payments:", len(payments))