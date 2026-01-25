SELECT info.top_genre FROM nominee_information info
    INNER JOIN ( SELECT nominee, COUNT(*) OVER (PARTITION BY nominee) AS n_winnings FROM oscar_nominees
        WHERE winner) tmp ON tmp.nominee = info.name
    ORDER BY n_winnings DESC, nominee ASC LIMIT 1;