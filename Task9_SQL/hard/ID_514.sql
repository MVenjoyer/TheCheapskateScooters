WITH t1 AS(SELECT *, MIN(created_at) OVER(PARTITION BY user_id) AS first_order, MIN(created_at)
    OVER(PARTITION BY user_id,product_id) AS prod_first_order, ABS(MIN(created_at) OVER(PARTITION
    BY user_id)-MIN(created_at)OVER(PARTITION BY user_id,product_id)) AS diff FROM marketing_campaign)
SELECT COUNT(DISTINCT user_id) FROM t1 WHERE diff >0