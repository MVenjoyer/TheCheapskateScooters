WITH cte AS (SELECT user_id FROM fact_events
    GROUP BY user_id HAVING ((COUNT(*) FILTER (
        WHERE event_type IN ('video call received', 'video call sent', 'voice call received', 'voice call sent')) * 1.0) / COUNT(*)) >= 0.5)
SELECT client_id FROM fact_events
    JOIN cte USING (user_id)
    GROUP BY client_id
    ORDER BY COUNT(*) DESC
    LIMIT 1