SELECT DISTINCT at1.user_id FROM amazon_transactions AS at1
    INNER JOIN amazon_transactions AS at2 ON at1.user_id = at2.user_id
    WHERE at1.created_at <> at2.created_at AND ABS(at1.created_at - at2.created_at) <= 7;
