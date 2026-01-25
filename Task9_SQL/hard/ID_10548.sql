WITH cte AS (SELECT actor_name,genre,avg_rating FROM (
    SELECT actor_name,genre,AVG(movie_rating) AS avg_rating, dense_rank() OVER(PARTITION BY actor_name ORDER BY COUNT(genre) DESC ,AVG(movie_rating) DESC) AS rnk FROM top_actors_rating group by 1,2)s
    WHERE rnk=1)
SELECT * FROM (SELECT *,dense_rank() OVER(ORDER BY avg_rating DESC) AS "rank"  FROM cte)
    WHERE rank<=3;