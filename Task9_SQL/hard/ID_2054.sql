WITH distinct_days AS (SELECT DISTINCT user_id, record_date AS date_h FROM sf_events
   ORDER BY user_id ASC, date_h ASC), consecutive_days AS
   (SELECT user_id, date_h - ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY date_h)::int AS date_h FROM distinct_days)
SELECT DISTINCT user_id FROM consecutive_days
    GROUP BY user_id, date_h
    HAVING COUNT(*) >= 3