SELECT cust_id, SUM(CASE WHEN state = 1 THEN -1.0*EXTRACT(epoch FROM timestamp)/3600
    ELSE 1.0*EXTRACT(epoch FROM timestamp)/3600 END) AS timediff FROM cust_tracking
    GROUP BY cust_id