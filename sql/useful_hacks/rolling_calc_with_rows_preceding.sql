-- Query returns Intercom ticket's rolling average CSAT score from previous 30 days

WITH calendar AS ( -- creating calendar dataset required for rolling calculations
    SELECT generate_series({{start_date}} - INTERVAL '30' DAY, {{end_date}}, '1 day'::interval) AS date_
)
, csat_daily AS ( -- caclualting rating sums and counts on daily level
    SELECT c.date_
    , SUM(t.rating) AS csat_sum
    , COUNT(t.rating) AS csat_count
    FROM calendar c
    LEFT JOIN intercom_tickets t ON c.date_ = t.ticket_created_at::date
    WHERE TRUE
    AND t.rating IS NOT NULL
    GROUP BY c.date_
)
, rolling_avg AS ( -- calculating rolling 30 days average rating on daily level
    SELECT date_
    , SUM(csat_sum) OVER (ORDER BY date_ ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
        / SUM(csat_count) OVER (ORDER BY date_ ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS rolling_30d_avg
    , SUM(csat_count) OVER (ORDER BY date_ ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS tickets_count
    FROM csat_daily
)
SELECT *
FROM rolling_avg
WHERE TRUE
AND date_ BETWEEN {{start_date}} AND {{end_date}}
ORDER BY date_ DESC
