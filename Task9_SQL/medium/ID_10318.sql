SELECT company_name, count20-count19 AS difference FROM
    (SELECT company_name,
        sum(CASE WHEN year='2019' THEN 1 END) AS count19,
        sum(CASE WHEN year='2020' THEN 1 END) AS count20
    FROM car_launches
    GROUP BY company_name) AS t1;