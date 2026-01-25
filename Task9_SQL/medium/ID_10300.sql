WITH t1 AS (
SELECT date,
    SUM((CASE WHEN paying_customer = 'yes' THEN downloads END)) AS paying_downloads,
    SUM((CASE WHEN paying_customer = 'no' THEN downloads END)) AS non_paying_downloads
FROM ms_user_dimension, ms_acc_dimension, ms_download_facts
    WHERE ms_user_dimension.acc_id = ms_acc_dimension.acc_id AND ms_user_dimension.user_id = ms_download_facts.user_id
GROUP BY date)
SELECT * FROM t1
    WHERE non_paying_downloads > paying_downloads
    ORDER BY date;