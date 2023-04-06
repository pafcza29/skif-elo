import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import mysql.connector

class Points(commands.Cog):

    def __init__(self, client):
        self.client = client

    testServerId = 1093176894515585206

    @nextcord.slash_command(name="test", description="A message for testing", guild_ids=[testServerId])
    async def test(self, interaction: Interaction):
        await interaction.response.send_message("Test message from COG!~")

    #Points in slash commands

    @nextcord.slash_command(name="points_add", description="DB stuff", guild_ids=[testServerId])
    async def points_add(self, interaction: Interaction, username: nextcord.User, count: int):
        guild = interaction.guild.id
        userid = str(username.id)
        try:
            connection = mysql.connector.connect(
                host='db4free.net',
                database='elo_bot',
                user='doobyuwu',
                password='laresistance29'
            )
            mySql_Create_Table_Query = "CREATE TABLE `elo_bot`.`DB_" + str(guild) + "` ( `Id` INT NOT NULL AUTO_INCREMENT , `User` VARCHAR(250) NOT NULL , `Points` SMALLINT NOT NULL , PRIMARY KEY (`Id`)) "
            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query)
            print(f"Guild ({guild}) Table created successfully")
        except mysql.connector.Error as error:
            print(f"Failed to create table in MySQL: {error}")
        finally:
            if connection.is_connected():
                table = "DB_" + str(guild)

                # Check if the user exists in the table
                sql = "SELECT * FROM " + table + " WHERE User = %s"
                val = (userid,)
                cursor.execute(sql, val)
                user = cursor.fetchone()

                # If the user doesn't exist, insert a new row with 0 points
                if user is None:
                    sql = "INSERT INTO " + table + " (User, Points) VALUES (%s, %s)"
                    val = (userid, 0)
                    cursor.execute(sql, val)
                    connection.commit()
                    print("New user added with 0 points")

                # Update the points for the user
                sql = "UPDATE " + table + " SET Points = Points + %s WHERE User = %s"
                val = (count, userid)
                cursor.execute(sql, val)
                connection.commit()
                print(cursor.rowcount, "record(s) updated")
            cursor.close()
            connection.close()
        await interaction.response.send_message(f"{count} points added to {username}")

    @nextcord.slash_command(name="points_remove", description="DB stuff", guild_ids=[testServerId])
    async def points_remove(self, interaction: Interaction, username: nextcord.User, count: int):
        guild = interaction.guild.id
        userid = str(username.id)
        try:
            connection = mysql.connector.connect(
                host='db4free.net',
                database='elo_bot',
                user='doobyuwu',
                password='laresistance29'
            )
            mySql_Create_Table_Query = "CREATE TABLE `elo_bot`.`DB_" + str(guild) + "` ( `Id` INT NOT NULL AUTO_INCREMENT , `User` VARCHAR(250) NOT NULL , `Points` SMALLINT NOT NULL , PRIMARY KEY (`Id`)) "
            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query)
            print(f"Guild ({guild}) Table created successfully")
        except mysql.connector.Error as error:
            print(f"Failed to create table in MySQL: {error}")
        finally:
            if connection.is_connected():
                table = "DB_" + str(guild)

                # Check if the user exists in the table
                sql = "SELECT * FROM " + table + " WHERE User = %s"
                val = (userid,)
                cursor.execute(sql, val)
                user = cursor.fetchone()

                # If the user doesn't exist, insert a new row with 0 points
                if user is None:
                    sql = "INSERT INTO " + table + " (User, Points) VALUES (%s, %s)"
                    val = (userid, 0)
                    cursor.execute(sql, val)
                    connection.commit()
                    print("New user added with 0 points")

                # Update the points for the user
                sql = "UPDATE " + table + " SET Points = Points - %s WHERE User = %s"
                val = (count, userid)
                cursor.execute(sql, val)
                connection.commit()
                print(cursor.rowcount, "record(s) updated")
            cursor.close()
            connection.close()
        await interaction.response.send_message(f"{count} points added to {username}")

    @nextcord.slash_command(name="points_check", description="Checks points of user", guild_ids=[testServerId])
    async def points_check(self, interaction: Interaction, username: nextcord.User):
        guild = interaction.guild.id
        userid = str(username.id)
        try:
            connection = mysql.connector.connect(
                host='db4free.net',
                database='elo_bot',
                user='doobyuwu',
                password='laresistance29'
            )
            mySql_Create_Table_Query = "CREATE TABLE `elo_bot`.`DB_" + str(guild) + "` ( `Id` INT NOT NULL AUTO_INCREMENT , `User` VARCHAR(250) NOT NULL , `Points` SMALLINT NOT NULL , PRIMARY KEY (`Id`)) "
            cursor = connection.cursor()
            result = cursor.execute(mySql_Create_Table_Query)
            print(f"Guild ({guild}) Table created successfully")
        except mysql.connector.Error as error:
            print(f"Failed to create table in MySQL: {error}")
        finally:
            if connection.is_connected():
                table = "DB_" + str(guild)

                # Check if the user exists in the table
                sql = "SELECT * FROM " + table + " WHERE User = %s"
                val = (userid,)
                cursor.execute(sql, val)
                user = cursor.fetchone()

                # If the user doesn't exist, insert a new row with 0 points
                if user is None:
                    await interaction.response.send_message(f"{username} does not have any records in DB.")
                    cursor.close()
                    connection.close()
                    return

                # Select points of user
                sql = "SELECT Points FROM " + table + " WHERE User = %s"
                val = (userid,)
                cursor.execute(sql, val)
                result = cursor.fetchone()
                count = result[0]
                print(count, "returned succesfully")
            cursor.close()
            connection.close()
        await interaction.response.send_message(f"{username} has total of {count} points")


    @nextcord.slash_command(name="top10", description="Returns top 10 users", guild_ids=[testServerId])
    async def top10(self, interaction: Interaction):
        guild = interaction.guild.id
        try:
            connection = mysql.connector.connect(
                host='db4free.net',
                database='elo_bot',
                user='doobyuwu',
                password='laresistance29'
            )
        except mysql.connector.Error as error:
            print(f"MySQL error: {error}")
        finally:
            if connection.is_connected():
                cursor = connection.cursor()
                table = "DB_" + str(guild)
                cursor.execute(f"SELECT User, Points FROM {table} ORDER BY Points DESC LIMIT 10")
                results = cursor.fetchall()

                # Create the embed
                embed = nextcord.Embed(title='Top 10 Users', color=0x458cff)
                for i, result in enumerate(results):
                    userid = int(result[0])
                    user = await self.client.fetch_user(userid)
                    username = f"{user.name}#{user.discriminator}"
                    points = result[1]
                    embed.add_field(name=f'{i+1}. {username}', value=f'{points} points', inline=False)
                print(f"Top 10 users returned")

            await interaction.response.defer()
            await interaction.followup.send(embed=embed)


def setup(client):
    client.add_cog(Points(client))
