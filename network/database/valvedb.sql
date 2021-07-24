create or replace table server
(
    id                nvarchar(18)   not null,
    mod_log           bool           not null,
    profanity_filter  bool           not null,
    message_log       bool           not null,
    spam_filter       bool           not null,
    mod_log_channel   nvarchar(18)   not null,
    ban_message       nvarchar(1000) not null,
    kick_message      nvarchar(1000) not null,
    prefix            nvarchar(50)   not null,
    force_ban_message nvarchar(1000) not null
);