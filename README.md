# Fiestura Business Analytics

## Project Overview

Fiestura Business Analytics is a data analytics project built using real operational data from Fiestura, an event management platform.

The project analyzes event registrations, category performance, attendee activity, payment records, and data quality to generate business insights.

## Tech Stack

- MySQL
- SQL (JOINs, GROUP BY, CTEs, Window Functions)
- Python
- Pandas
- Matplotlib
- Jupyter Notebook

## Dataset

The project uses three datasets:

- Events
- Registrations
- Payments

The current exported dataset contains:
- 16 events
- 25 registrations
- 25 payment records

## Business Questions

1. Which events attract the most registrations?
2. Which event categories perform best?
3. How do registrations change month over month?
4. How many attendees register for multiple events?
5. What payment amounts are recorded against events?
6. What data-quality issues affect the analysis?

## Key Findings

- Pace recorded 7 registrations, the highest among exported events.
- The category labelled `ongoing` recorded 7 registrations; its classification requires verification.
- March recorded the highest registration activity with 14 registrations.
- The exported dataset contains 13 unmatched registration references and 4 unmatched payment references.
- Total recorded payment amount was ₹647. Payment status was unavailable, so this is not treated as verified revenue.

## Data Quality Limitations

Some registration and payment records reference event IDs absent from the exported events dataset.

The original records are preserved. Event-level analyses use matching event references, while overall registration trends retain all registration records.

The payment export does not contain transaction status. Consequently, payment success rates and verified revenue cannot be calculated.

## Project Structure

```text
fiestura-business-analytics/
├── data/
├── sql/
│   ├── schema.sql
│   └── analysis.sql
├── notebooks/
│   └── fiestura_analysis.ipynb
├── visualizations/
├── clean_data.py
├── import_data.py
└── README.md
```

## Conclusion

This project demonstrates an end-to-end analytics workflow involving data extraction, cleaning, SQL-based analysis, Python exploration, visualization, and business recommendations.
