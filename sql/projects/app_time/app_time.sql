WITH actions_data AS ( -- getting actions from chosen timeframe
    SELECT a.user_id
    , a.action_at::date AS date
    , a.event_name
    , a.action_at
    , COALESCE(a.other_params ->> 'screen_name', 'is_null') AS flow
    , a.id AS action_id
    , s.id AS session_id
    FROM app_actions a
    JOIN app_actions_mapping m ON a.event_name = m.event_name
    JOIN app_actions_sessions s ON s.count_events > 1
                                AND s.start_at BETWEEN '{window_start}' AND '{window_end}'
                                AND a.action_at BETWEEN s.start_at AND s.end_at
                                AND a.user_id = s.user_id
    WHERE TRUE
    AND a.action_at BETWEEN '{window_start}' AND '{window_end}'
    AND a.user_id = ANY(ARRAY{user_list})
)
, actions_mapped AS ( -- assigning lvl 1 and lvl 2 activities
    SELECT DISTINCT a.*
    , m.app_time_lvl1
    , m.app_time_lvl2
    FROM actions_data a
    JOIN app_actions_mapping m ON a.event_name = m.event_name AND a.flow = m.flow
)
, actions_final AS ( -- checking when next action took place
    SELECT user_id
    , date
    , action_id
    , session_id
    , app_time_lvl1
    , app_time_lvl2
    , action_at
    , LEAD(action_at) OVER (PARTITION BY user_id, session_id ORDER BY action_at) AS next_action_at
    FROM actions_mapped
)
, app_time_base AS ( -- calculating app time for each event
    SELECT user_id
    , date
    , app_time_lvl1
    , app_time_lvl2
    , (DATE_PART('minute', next_action_at - action_at) * 60 +
            DATE_PART('second', next_action_at - action_at)) / 60 AS app_time
    FROM actions_final
    WHERE TRUE
    AND next_action_at IS NOT NULL
    AND action_at != next_action_at
)
, FINAL AS (
    SELECT date
    , user_id
    , SUM(app_time) AS total_time
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'investing' THEN app_time END), 0) AS investing
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'investing' AND app_time_lvl2 = 'exploration' THEN app_time END), 0) AS investing_exploration
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'investing' AND app_time_lvl2 = 'funds' THEN app_time END), 0) AS investing_funds
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'investing' AND app_time_lvl2 = 'orders' THEN app_time END), 0) AS investing_orders
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'social' THEN app_time END), 0) AS social
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'social' AND app_time_lvl2 = 'education' THEN app_time END), 0) AS social_education
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'social' AND app_time_lvl2 = 'engagement' THEN app_time END), 0) AS social_engagement
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'social' AND app_time_lvl2 = 'feed_activity' THEN app_time END), 0) AS social_feed_activity
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'social' AND app_time_lvl2 = 'followers' THEN app_time END), 0) AS social_followers
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'other' THEN app_time END), 0) AS other
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'other' AND app_time_lvl2 = 'account' THEN app_time END), 0) AS other_account
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'other' AND app_time_lvl2 = 'app_exploration' THEN app_time END), 0) AS other_app_exploration
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'other' AND app_time_lvl2 = 'authorization' THEN app_time END), 0) AS other_authorization
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'other' AND app_time_lvl2 = 'kyc' THEN app_time END), 0) AS other_kyc
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'other' AND app_time_lvl2 = 'profile' THEN app_time END), 0) AS other_profile
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'other' AND app_time_lvl2 = 'not_defined' THEN app_time END), 0) AS other_not_defined
    , COALESCE(SUM(CASE WHEN app_time_lvl1 = 'other' AND app_time_lvl2 = 'support' THEN app_time END), 0) AS other_support
    FROM app_time_base
    GROUP BY date, user_id
)

/* Update existing records */
INSERT INTO app_time
    (date, user_id, total_time, investing, investing_exploration, investing_funds, investing_orders,
     social, social_education, social_engagement, social_feed_activity, social_followers, other, other_account,
     other_app_exploration, other_authorization, other_kyc, other_not_defined, other_profile, other_support)
    SELECT * FROM FINAL

ON CONFLICT (date, user_id) DO UPDATE
SET (total_time, investing, investing_exploration, investing_funds, investing_orders,
     social, social_education, social_engagement, social_feed_activity, social_followers, other, other_account,
     other_app_exploration, other_authorization, other_kyc, other_not_defined, other_profile, other_support) =
     (EXCLUDED.total_time, EXCLUDED.investing, EXCLUDED.investing_exploration, EXCLUDED.investing_funds, EXCLUDED.investing_orders,
     EXCLUDED.social, EXCLUDED.social_education, EXCLUDED.social_engagement, EXCLUDED.social_feed_activity, EXCLUDED.social_followers, EXCLUDED.other, EXCLUDED.other_account,
     EXCLUDED.other_app_exploration, EXCLUDED.other_authorization, EXCLUDED.other_kyc, EXCLUDED.other_not_defined, EXCLUDED.other_profile, EXCLUDED.other_support)

RETURNING *
;
