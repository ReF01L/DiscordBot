import discord
from DiscordBot import config, const, answers, command

from discord import utils


class MyClient(discord.Client):
    def get_role_by_author(self, author, cs):
        for role in author.roles:
            if role.name.startswith(const.cs) and cs:
                return role.name[role.name.index(const.cs) + len(const.cs):len(role.name)]
            if role.name.startswith(const.dota) and not cs:
                return role.name[role.name.index(const.dota) + len(const.dota):len(role.name)]

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content == command.WANNA_CS:
            # id хочет-играть канала
            await client.get_channel(699681473858371605) \
                .send(answers.WANNA_CS.format(message.author.display_name,
                                              self.get_role_by_author(message.author, 1)))
        elif message.content == command.WANNA_DOTA:
            # id хочет-играть канала
            await client.get_channel(699681473858371605) \
                .send(answers.WANNA_DOTA.format(message.author.display_name,
                                                self.get_role_by_author(message.author, 0)))

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            if len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER:
                await member.add_roles(role)
                print('[SUCCESS] User {0} has been granted with role {1}'.format(member.display_name, role.name))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for {0}'.format(member.display_name))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=config.ROLES[emoji])

            await member.remove_roles(role)
            print('[SUCCESS] Role {1} has been remove for user {0}'.format(member.display_name, role.name))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


client = MyClient()
client.run(config.TOKEN)
