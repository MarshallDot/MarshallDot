import mariadb

mariad = mariadb.connect(user="root", password="example", host="localhost", port=4004)


def createTables():
    cursor = mariad.cursor()
    cursor.execute("USE marshall")
    cursor.execute("""
                    create or replace table server (
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
                    """)
    cursor.execute("""
                    create or replace table log (
                        id        nvarchar(18)   not null,
                        server_id nvarchar(18)   not null,
                        type      nvarchar(100)  not null,
                        log       nvarchar(1800) not null
                    );
                   """)
    mariad.commit()
