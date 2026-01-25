WITH base_tbl AS (
SELECT player_id,match_result,
       ROW_NUMBER() OVER(PARTITION BY player_id ORDER BY match_date) as game_number,
       ROW_NUMBER() OVER(PARTITION BY player_id ORDER BY match_date) - ROW_NUMBER() OVER(PARTITION BY player_id, match_result ORDER BY match_date) as grp_id
FROM players_results),streak_tbl AS (SELECT player_id,grp_id,COUNT(*) as streak_len FROM base_tbl
    WHERE match_result = 'W'
    GROUP BY 1, 2)
SELECT player_id,streak_len FROM  streak_tbl
    WHERE streak_len IN (SELECT MAX(streak_len) FROM streak_tbl)