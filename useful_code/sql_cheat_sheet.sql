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

-- ##### WINDOW FUNCTIONS #####

-- ROW_NUMBER
SELECT *
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
  FROM transactions
) t
WHERE rn = 1;

-- RANK
SELECT *,
RANK() OVER (
    ORDER BY amount DESC
) AS rnk
FROM transactions;
-- If amounts = 100,100,80 → ranks = 1,1,3

-- DENSE_RANK
DENSE_RANK() OVER (ORDER BY amount DESC)
-- Same rank for ties, no gaps. 100,100,80 → 1,1,2

-- SUM() OVER()
SELECT *,
SUM(amount) OVER (
    PARTITION BY user_id
    ORDER BY txn_date
) AS running_total
FROM transactions;
-- Running totals or grouped totals without collapsing rows

-- AVG() OVER()
SELECT *,
AVG(amount) OVER (
    PARTITION BY user_id
) AS avg_user_spend
FROM transactions;
-- Average by group while keeping rows

-- COUNT() OVER()
SELECT *,
COUNT(*) OVER (
    PARTITION BY user_id
) AS txn_count
FROM transactions;
-- Count rows in partition

-- MIN() / MAX() OVER()
MIN(txn_date) OVER (
    PARTITION BY user_id
) AS first_txn
-- Earliest / latest value without GROUP BY.

--LAG
SELECT 
  user_id,
  amount,
  LAG(amount) OVER (PARTITION BY user_id ORDER BY date) AS prev_amount
FROM transactions;
-- Previous row value

-- LEAD
LEAD(txn_date) OVER (
    PARTITION BY user_id
    ORDER BY txn_date
) AS next_txn
-- Next row value

-- NTILE(n)
NTILE(4) OVER (
    ORDER BY amount DESC
) AS quartile
-- Split into buckets (quartiles, deciles)

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

-- DATE MANIPULATION

TO_CHAR(trans_date, 'YYYY-MM') AS month
