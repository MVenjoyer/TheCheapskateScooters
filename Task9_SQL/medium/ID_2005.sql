SELECT SUM(CASE WHEN country = 'USA' AND status = 'open' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS us_active_share
    FROM fb_active_users