import os
import discord
from configuration import (get_user_name, get_password, get_user_name, get_host, get_database)
import mysql.connector


def update_users(guild_members):
    db = mysql.connector.connect(user=get_user_name(
    ), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()

    for Member in guild_members:
        if not Member.bot and Member.guild.id == 759715539622428673:
            sql.execute(f"""
            REPLACE INTO users(id, name, avatar_url) values("{Member.id}", "{Member.name}", "{Member.avatar_url}")
            """)
    db.commit()
    sql.close()

def get_voice_channels() -> list:
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    # Example: "active_vc" is row[0]
    sql.execute(
        "SELECT active_vc FROM voice_channels")
    rows = sql.fetchall()

    active_vc = []

    sql.close()
    for row in rows:
        active_vc.append(row[0])
    return active_vc

def add_vc(active_vc, message_channel_id, message_id):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    sql.execute(f"""
    INSERT INTO voice_channels (active_vc, channel_id, message_id) values ({active_vc}, {message_channel_id}, {message_id})
    """)
    db.commit()
    sql.close()

def get_command_message(delete_vc):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    sql.execute(f"""
    SELECT channel_id, message_id 
    FROM voice_channels
    WHERE active_vc={delete_vc};
    """)
    IDs = sql.fetchall()
    message_id = IDs[0][1]
    channel_id = IDs[0][0]
    message = {
        "id": message_id,
        "channel": channel_id
    }
    sql.close()
    return message

def remove_vc(delete_vc):
    db = mysql.connector.connect(user=get_user_name(), password=get_password(), host=get_host(), database=get_database())
    sql = db.cursor()
    sql.execute(f"""
    DELETE FROM voice_channels WHERE active_vc={delete_vc}
    """)
    db.commit()
    sql.close()
