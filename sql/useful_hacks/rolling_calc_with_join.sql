-- Query checks average lengths (by number of messages sent) of chats between premium investors and their followers
-- Rolling 7 and 30 days average calculated

WITH ambassadors AS ( -- selecting premium investors
    SELECT id AS ambassador_id
    FROM backend.users
    WHERE TRUE
    AND is_ambassador IS TRUE
)
, messages_base AS ( -- selecting user-premium investor pairs who chatted with each other
    SELECT m.user_id_received AS user_id
    , m.user_id_sent AS ambassador_id
    , m.channel_id
    , m.message_created_at
    FROM getstream_private_messages m
    JOIN ambassadors a ON m.user_id_sent = a.ambassador_id
    UNION ALL
    SELECT m.user_id_sent AS user_id
    , m.user_id_received AS ambassador_id
    , m.channel_id
    , m.message_created_at
    FROM getstream_private_messages m
    JOIN ambassadors a ON m.user_id_received = a.ambassador_id
)
, chats_base AS ( -- counting number of messages on chat level
    SELECT m.user_id
    , m.ambassador_id
    , m.channel_id
    , MIN(m.message_created_at)::date AS date_
    , COUNT(m.message_created_at) AS msg_count
    FROM messages_base m
    JOIN backend.users u ON m.user_id = u.id AND u.is_analytics_relevant IS TRUE
    GROUP BY m.user_id, m.ambassador_id, m.channel_id
)
, dates AS ( -- generating date series
    SELECT generate_series({{start_date}} - 29, {{end_date}}, '1 day'::interval) AS date_
)
, data_30days as ( -- assigning chat length to chat created date and next 29 days
SELECT d.date_
, c.channel_id AS chat_id
, c.msg_count AS msg_30d
FROM dates d
LEFT JOIN chats_base c ON d.date_ BETWEEN c.date_ AND c.date_ + interval '29' day
)
, data_7days as ( -- assigning chat length to chat created date and next 6 days
SELECT d.date_
, c.channel_id AS chat_id
, c.msg_count AS msg_7d
FROM dates d
LEFT JOIN chats_base c ON d.date_ BETWEEN c.date_ AND c.date_ + interval '6' day
)
, final_dataset AS ( -- calculating average and median length + chats count for each date
    SELECT d.date_
    , AVG(d2.msg_7d) AS avg_length_7d
    , percentile_cont(0.5) within group (order by msg_7d) as median_length_7d
    , COUNT(d2.msg_7d) AS chat_count_7d
    , AVG(d1.msg_30d) AS avg_length_30d
    , percentile_cont(0.5) within group (order by msg_30d) as median_length_30d
    , COUNT(d1.msg_30d) AS chat_count_30d
    FROM dates d
    LEFT JOIN data_30days d1 ON d.date_ = d1.date_
    LEFT JOIN data_7days d2 ON d.date_ = d2.date_ AND d1.chat_id = d2.chat_id
    GROUP BY d.date_
)
SELECT *
FROM final_dataset
WHERE TRUE
AND date_ BETWEEN {{start_date}} AND {{end_date}}
