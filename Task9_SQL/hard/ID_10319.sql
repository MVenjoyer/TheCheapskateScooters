WITH month_agg AS (SELECT TO_CHAR(created_at, 'YYYY-MM') AS year_month, SUM(value) AS month_total FROM sf_transactions
    GROUP BY year_month
    ORDER BY year_month)

SELECT year_month, ((month_total - LAG(month_total) OVER ()) / LAG(month_total) OVER ()) * 100.00 AS revenue_diff_pct FROM month_agg;