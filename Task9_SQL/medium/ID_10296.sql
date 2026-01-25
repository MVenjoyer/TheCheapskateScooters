SELECT AVG(CASE WHEN status = 'closed' THEN 1 ELSE 0 END) AS ratio_closed FROM fb_account_status
    WHERE status_date = '2020-01-10'