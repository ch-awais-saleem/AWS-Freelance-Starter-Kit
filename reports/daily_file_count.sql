SELECT
    date(from_iso8601_timestamp(event_time)) AS process_date,
    COUNT(*) AS files_processed
FROM glue_job_run_logs
GROUP BY process_date
ORDER BY process_date DESC;
