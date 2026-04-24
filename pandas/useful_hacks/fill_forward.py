def fill_forward_handler(onal args from here
    asset_type: str,
    window_start: Optional[str] = None,
    window_end: Optional[str] = None,
):
    today = date.today()
    if window_start is None:
        window_start = today - timedelta(days=30)

    if window_end is None:
        window_end = today - timedelta(days=1)

    read_conn = PostgresConnector(Databases.delta_replica)
    write_conn = PostgresConnector(Databases.delta_main)

    query = PostgresConnector.read_query_from_file(
        QUERIES_FOLDER / "get_mutual_funds_prices.sql",
        window_start=window_start,
        window_end=window_end,
        asset_type=asset_type,
    )

    df = read_conn.sql_to_pandas(query)

    # fill forwarding close price from last known close
    df = df.sort_values(["instrument_id", "date"])
    df["close"] = df.groupby("instrument_id")["close"].ffill()

    # leave only fill forwarded records where close is not null
    df = df[df["is_fill_forwarded"] == True] # f.close IS NULL AS is_fill_forwarded <- condition in query
    df.dropna(subset=["close"], inplace=True)

    df.drop(columns=["is_fill_forwarded"], inplace=True)

    # add fill_forward as price source
    df["source"] = "fill_forward"
    df["created"] = pd.Timestamp.now(tz="UTC")

    msg = "No records updated"
    if len(df) > 0:
        # Upload without update
        write_conn.copy_expert_from_pandas(
            source=df,
            destination="stocks_prices_daily",
            update_on_conflict=False,
            constraint_cols=["date", "instrument_id"],
        )

        msg = f"{len(df)} records updated"

    return msg
