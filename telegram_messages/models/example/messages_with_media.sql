-- models/messages_with_media.sql

{{ config(materialized='view') }}

SELECT
    message_id,
    channel_username,
    sender_id,
    message,
    message_date,
    media_path,
    emoji_used
FROM
    {{ source('public', 'telegram_messages') }}
WHERE
    media_path IS NOT NULL
ORDER BY
    message_date DESC
