-- models/youtube_activity_summary.sql

{{ config(materialized='table') }}

SELECT
    channel_username,
    COUNT(*) AS total_messages_with_youtube_links,
    MIN(message_date) AS first_youtube_link,
    MAX(message_date) AS latest_youtube_link
FROM
    {{ source('public', 'telegram_messages') }}
WHERE
    youtube_links IS NOT NULL
GROUP BY
    channel_username
ORDER BY
    total_messages_with_youtube_links DESC
