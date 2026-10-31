SELECT
    e.title,
    e.category,
    COUNT(r.registration_id) AS total_registrations
FROM staging_events e
LEFT JOIN staging_registrations r
    ON e.event_id = r.event_id
GROUP BY e.event_id, e.title, e.category
ORDER BY total_registrations DESC;


SELECT
    e.category,
    COUNT(r.registration_id) AS total_registrations
FROM staging_events e
LEFT JOIN staging_registrations r
    ON e.event_id = r.event_id
GROUP BY e.category
ORDER BY total_registrations DESC;


SELECT
    DATE_FORMAT(created_at, '%Y-%m') AS registration_month,
    COUNT(*) AS total_registrations
FROM staging_registrations
GROUP BY DATE_FORMAT(created_at, '%Y-%m')
ORDER BY registration_month;


SELECT
    user_id,
    COUNT(DISTINCT event_id) AS events_registered
FROM staging_registrations
GROUP BY user_id
HAVING COUNT(DISTINCT event_id) > 1
ORDER BY events_registered DESC;


SELECT
    e.title,
    COUNT(p.payment_id) AS payment_attempts,
    SUM(p.amount) AS recorded_payment_amount
FROM staging_events e
LEFT JOIN staging_payments p
    ON e.event_id = p.event_id
GROUP BY e.event_id, e.title
ORDER BY recorded_payment_amount DESC;


SELECT
    r.event_id,
    COUNT(*) AS registration_count,
    COUNT(DISTINCT r.user_id) AS unique_users
FROM staging_registrations r
LEFT JOIN staging_events e
    ON r.event_id = e.event_id
WHERE e.event_id IS NULL
GROUP BY r.event_id
ORDER BY registration_count DESC;

SELECT
    p.event_id,
    COUNT(*) AS payment_attempts,
    SUM(p.amount) AS recorded_amount,
    COUNT(DISTINCT p.user_id) AS unique_users
FROM staging_payments p
LEFT JOIN staging_events e
    ON p.event_id = e.event_id
WHERE e.event_id IS NULL
GROUP BY p.event_id
ORDER BY payment_attempts DESC;


SELECT
    'Registrations' AS data_source,
    COUNT(*) AS total_records,
    SUM(e.event_id IS NULL) AS unmatched_records
FROM staging_registrations r
LEFT JOIN staging_events e
    ON r.event_id = e.event_id

UNION ALL

SELECT
    'Payments',
    COUNT(*),
    SUM(e.event_id IS NULL)
FROM staging_payments p
LEFT JOIN staging_events e
    ON p.event_id = e.event_id;