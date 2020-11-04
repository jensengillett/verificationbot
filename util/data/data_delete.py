import os


def delete_database_guild(guild_id: str):
    folder_name = "data"
    prefix = "guild_"
    path = f"{folder_name}/{prefix}{guild_id}.db"
    if os.path.exists(path):
        os.remove(path)
