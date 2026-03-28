-- Basic aggregation

SELECT column, COUNT(*), SUM(amount), AVG(amount)
FROM table
GROUP BY column
-- HAVING SUM(amount) > 1000; optional filter

-- Conditional aggregation

SELECT 
  user_id,
  SUM(CASE WHEN status = 'success' THEN amount ELSE 0 END) AS success_amount
FROM transactions
GROUP BY user_id;

-- Window functions

SELECT *
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
  FROM transactions
) t
WHERE rn = 1;

-- RANK() OVER (ORDER BY total_spend DESC) - ranking
-- SUM(amount) OVER (PARTITION BY user_id ORDER BY date) - running total

-- Lag/Lead

SELECT 
  user_id,
  amount,
  LAG(amount) OVER (PARTITION BY user_id ORDER BY date) AS prev_amount
FROM transactions;

-- Rolling windows

SELECT
    user_id,
    login_date,
    AVG(daily_logins) OVER (
        PARTITION BY user_id
        ORDER BY login_date
        RANGE BETWEEN INTERVAL '29 days' PRECEDING AND CURRENT ROW
    ) AS rolling_avg_30d
FROM (
    SELECT
        user_id,
        login_date,
        COUNT(*) AS daily_logins
    FROM logins
    GROUP BY user_id, login_date
) t
ORDER BY user_id, login_date;

-- + generate series if lack of continous dates

SELECT generate_series(
    MIN(login_date),
    MAX(login_date),
    INTERVAL '1 day'
)
