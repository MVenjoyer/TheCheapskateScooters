SELECT video_id,reviewed_times FROM (
    SELECT video_id, RANK() OVER (ORDER BY COUNT(u.flag_id) DESC),
        COUNT(CASE WHEN reviewed_by_yt = 'TRUE' THEN u.flag_id END) AS reviewed_times
    FROM user_flags AS u INNER JOIN flag_review AS f ON u.flag_id = f.flag_id
        GROUP BY video_id) WHERE rank = 1
