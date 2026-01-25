SELECT business_postal_code,
    COUNT(DISTINCT REGEXP_REPLACE( LOWER(business_address), '\d+ | .+', '', 'g' )) AS counter
    FROM sf_restaurant_health_violations WHERE business_postal_code IS NOT NULL
    GROUP BY business_postal_code ORDER BY counter DESC