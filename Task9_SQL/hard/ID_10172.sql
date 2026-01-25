WITH cte AS (SELECT sub.*, DENSE_RANK() OVER(PARTITION BY sub.months ORDER BY sub.total_sale DESC) AS rnks  FROM
    (SELECT EXTRACT('month' FROM a.invoicedate) AS months, a.description, SUM(a.unitprice*a.quantity) AS total_sale
    FROM online_retail AS a
    GROUP BY 1, 2 ORDER BY 1, 2) AS sub)
SELECT cte.months, cte.description, cte.total_sale  FROM cte
    WHERE cte.rnks = 1