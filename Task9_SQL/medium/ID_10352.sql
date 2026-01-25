WITH min_max AS (SELECT user_id,DATE(timestamp),
    MAX(CASE
        WHEN action = 'page_load' THEN timestamp
        END) AS pg_load,
    MIN(CASE
        WHEN action = 'page_exit' THEN timestamp
        END)  AS pg_exit
    FROM facebook_web_log GROUP BY 1,2)

SELECT user_id,AVG(pg_exit-pg_load) AS avg_session_time
    FROM min_max
    GROUP BY 1 HAVING AVG(pg_exit-pg_load) IS NOT NULL