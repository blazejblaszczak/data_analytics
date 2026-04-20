WITH actions_base AS ( -- counting actions and adding flow column
    SELECT action_type
    , param_name
    , param_value
    , COALESCE(other_params ->> 'screen_name', 'is_null') AS flow
    , event_name
    FROM app_actions
    WHERE TRUE
    AND action_at >= CURRENT_DATE - 15
    AND user_id IS NOT NULL
    AND param_value IS NOT NULL
    -- excluding not relevant action types
    AND action_type NOT IN ('app-state-change', 'network-state-change', 'deep-link-handled', 'startup-time', 'error', 'scroll')
    AND param_name NOT IN ('direction')
    AND param_value NOT IN ('pin_required_screen', 'success', 'summary', 'header_back_arrow', 'header_back_arrow_default',
                            'welcome', 'edit', 'search_search_results', 'lock_screen_numpad_digit', 'app_lock_screen_numpad_digit')
    GROUP BY action_type, param_name, param_value, flow, event_name
    HAVING COUNT(id) > 100
)
SELECT *
, COALESCE(
    -- firstly we assign groups based on param_value
    CASE WHEN param_value ILIKE '%kyc%' OR param_value ILIKE '%verify_email%'
        THEN 'other'
    WHEN param_value ILIKE '%commun%' OR param_value ILIKE '%friend%'
        OR param_value ILIKE '%referr%' OR param_value ILIKE '%article%'
        OR param_value ILIKE '%chat%' OR param_value ILIKE '%comment%'
        OR param_value ILIKE '%gif%' OR param_value ILIKE '%like%'
        OR param_value ILIKE '%analyst%' OR param_value ILIKE '%news%'
        OR param_value ILIKE '%invit%' OR param_value ILIKE '%follow%'
        OR (param_value ILIKE '%activity%' AND param_value NOT ILIKE '%instrument_activity%')
        OR param_value IN ('recent_feed', 'trending_feed') OR param_value ILIKE '%top_investor%'
        THEN 'social'
    WHEN param_value ILIKE '%invest%' OR param_value ILIKE '%instrum%'
        OR param_value ILIKE '%buy%' OR param_value ILIKE '%sell%'
        OR param_value ILIKE '%watchlist%' OR param_value ILIKE '%collection%'
        OR param_value ILIKE '%stock%' OR param_value ILIKE '%asset%'
        OR param_value ILIKE '%payment%' OR param_value ILIKE '%price%'
        OR param_value ILIKE '%topup%' OR param_value ILIKE '%withdraw%'
        OR param_value ILIKE '%mover%' OR param_value ILIKE '%bank%'
        OR param_value ILIKE '%order%' OR param_value ILIKE '%money%'
        OR param_value ILIKE '%transaction%' OR param_value ILIKE '%amount%'
        OR param_value ILIKE '%top_up%' OR param_value ILIKE '%debit%'
        OR param_value ILIKE '%chart%' OR param_value ILIKE '%portfolio%'
        OR param_value ILIKE '%porfolio%' OR param_value ILIKE '%sharing_compet%'
        OR param_value ILIKE '%currenc%' OR param_value = 'lists'
        OR param_value ILIKE '%statement%' OR param_value ILIKE '%most_popular%'
        OR param_value ILIKE '%trade%' OR param_value ILIKE '%funding%'
        OR param_value ILIKE '%deposit%' OR param_value ILIKE '%dividend%'
        THEN 'investing'
    WHEN param_value ILIKE '%searchbar%' OR param_value ILIKE '%account%'
        OR param_value ILIKE '%other_profile%' OR param_value ILIKE '%profile_options%'
        OR param_value ILIKE '%explore%'
        THEN 'other' END,
    -- secondly, for actions without param_value assignment, we assign group based on other_params value
    CASE WHEN flow ILIKE '%kyc%'
        THEN 'other'
    WHEN flow ILIKE '%commun%' OR flow ILIKE '%chat%'
        OR flow ILIKE '%news%' OR flow ILIKE '%article%'
        OR flow ILIKE '%friend%' OR flow ILIKE '%invit%'
        OR (flow ILIKE '%activity%' AND flow NOT ILIKE '%instrument_activity%')
        OR flow ILIKE '%follow%'
        THEN 'social'
    WHEN flow ILIKE '%invest%' OR flow ILIKE '%instrum%'
        OR flow ILIKE '%price%' OR flow = 'home'
        OR flow ILIKE '%amount%' OR flow ILIKE '%transaction%'
        OR flow ILIKE '%watchlist%' OR flow ILIKE '%statement%'
        OR flow ILIKE '%topup%' OR flow ILIKE '%withdraw%'
        OR flow ILIKE '%money%' OR flow ILIKE '%collection%'
        OR flow ILIKE '%bank%' OR flow ILIKE '%payment%'
        OR flow ILIKE '%mover%' OR flow ILIKE '%trade%'
        OR flow ILIKE '%portfolio%' OR flow ILIKE '%stock%'
        OR flow = 'lists'
        THEN 'investing'
    ELSE 'other' END) AS app_time_lvl1
, COALESCE(
    -- firstly we assign groups based on param_value
    CASE WHEN param_value ILIKE '%kyc%' OR param_value IN ('select_country_modal')
        THEN 'kyc'
    WHEN param_value ILIKE '%news%' OR param_value ILIKE '%analyst%'
        OR param_value ILIKE '%article%'
        THEN 'education'
    WHEN param_value ILIKE '%friend%' OR param_value ILIKE '%referr%'
        OR param_value ILIKE '%chat%' OR param_value ILIKE '%invit%'
        OR param_value ILIKE '%follow%'
        THEN 'followers'
    WHEN param_value ILIKE '%comment%' OR param_value ILIKE '%gif%'
        OR param_value ILIKE '%like%' OR param_value ILIKE '%top_investor%'
        THEN 'engagement'
    WHEN (param_value ILIKE '%activity%' AND param_value NOT ILIKE '%instrument_activity%')
        OR param_value ILIKE '%commun%' OR param_value IN ('recent_feed', 'trending_feed')
        THEN 'feed_activity'
    WHEN param_value ILIKE '%topup%' OR param_value ILIKE '%withdraw%'
        OR param_value ILIKE '%payment%' OR param_value ILIKE '%money%'
        OR param_value ILIKE '%bank%' OR param_value ILIKE '%transaction%'
        OR param_value ILIKE '%top_up%' OR param_value ILIKE '%debit%'
        OR param_value ILIKE '%funding%' OR param_value ILIKE '%deposit%'
        THEN 'funds'
    WHEN param_value ILIKE '%buy%' OR param_value ILIKE '%sell%'
        OR param_value ILIKE '%order%' OR param_value ILIKE '%trade%'
        OR param_value ILIKE '%stock%'
        THEN 'orders'
    WHEN param_value ILIKE '%invest%' OR param_value ILIKE '%instrum%'
        OR param_value ILIKE '%watchlist%' OR param_value ILIKE '%collection%'
        OR param_value ILIKE '%asset%' OR param_value ILIKE '%amount%'
        OR param_value ILIKE '%price%' OR param_value ILIKE '%mover%'
        OR param_value ILIKE '%chart%' OR param_value ILIKE '%portfolio%'
        OR param_value ILIKE '%porfolio%' OR param_value ILIKE '%sharing_compet%'
        OR param_value ILIKE '%currenc%' OR param_value ILIKE '%most_popular%'
        OR param_value = 'lists' OR param_value ILIKE '%statement%'
        OR param_value ILIKE '%dividend%'
        THEN 'exploration'
    WHEN param_value ILIKE '%support%' OR param_value ILIKE '%terms%'
        OR param_value ILIKE '%data privacy%' OR param_value ILIKE '%policie%'
        OR param_value ILIKE '%intercom%'
        THEN 'support'
    WHEN param_value ILIKE '%sign%' OR (param_value ILIKE '%email%' AND param_value ILIKE '%verif%')
        OR param_value ILIKE '%lock_screen%'
        THEN 'authorization'
    WHEN param_value ILIKE '%explore%' OR param_value ILIKE '%notificat%'
        OR param_value ILIKE '%searchbar%'
        OR param_value IN ('search_section', 'activation-banner', 'banners_list')
        THEN 'app_exploration'
    WHEN param_value ILIKE '%profile%'
        THEN 'profile'
    WHEN param_value ILIKE '%account%'
        THEN 'account' END,
    -- secondly, for actions without param_value assignment, we assign group based on other_params value
    CASE WHEN flow ILIKE '%kyc%'
        THEN 'kyc'
    WHEN flow ILIKE '%chat%' OR flow ILIKE '%friend%'
        OR flow ILIKE '%invit%' OR flow ILIKE '%follow%'
        THEN 'followers'
    WHEN flow ILIKE '%news%'
        THEN 'education'
    WHEN (flow ILIKE '%activity%' AND flow NOT ILIKE '%instrument_activity%')
        OR flow ILIKE '%commun%'
        THEN 'feed_activity'
    WHEN flow ILIKE '%invest%' OR flow = 'home'
        OR flow ILIKE '%amount%' OR flow ILIKE '%watchlist%'
        OR flow ILIKE '%statement%' OR flow ILIKE '%instrum%'
        OR flow ILIKE '%collection%' OR flow = 'lists'
        OR flow ILIKE '%mover%' OR flow ILIKE '%trade%'
        OR flow ILIKE '%portfolio%' OR flow ILIKE '%stock%'
        OR flow ILIKE '%price%'
        THEN 'exploration'
    WHEN flow ILIKE '%topup%' OR flow ILIKE '%withdraw%'
        OR flow ILIKE '%money%' OR flow ILIKE '%transaction%'
        OR flow ILIKE '%bank%' OR flow ILIKE '%payment%'
        THEN 'funds'
    WHEN flow = 'auth' OR flow ILIKE '%sign%'
        OR flow ILIKE '%apptrack%' OR flow ILIKE '%pin%'
        OR (flow ILIKE '%email%' AND flow ILIKE '%verif%')
        THEN 'authorization'
    WHEN flow ILIKE '%profile%'
        THEN 'profile'
    WHEN flow ILIKE '%explor%' OR flow ILIKE 'home'
        THEN 'app_exploration'
    WHEN flow ILIKE '%account%'
        THEN 'account'
    ELSE 'not_defined' END
    ) AS app_time_lvl2
FROM actions_base
