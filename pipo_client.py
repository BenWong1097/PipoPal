import discord
from repl_db import ReplDB

class PipoClient(discord.Client):
  async def on_ready(self):
    print("Logged in as {0}!".format(self.user))
    self.db = ReplDB()
  async def on_message(self, message):
    print("Message from {0.author}: {0.content}".format(message))
    print(message.author.id)
    msg = message.content.lower()
    # "ppp" is the bot command prefix
    if not msg.startswith("ppp"):
      return
    # Ignore empty commands
    args = msg.split(' ')[1:]
    if len(args) < 1:
      return
    
    print("Command {0}".format(','.join(args)))
    # ppp create @Player2
    if args[0] == "create":
      await self.cmd_create_room(message)
    elif args[0] == "name":
      await self.cmd_rename_room(message)
  async def cmd_rename_room(self, message):
    '''
    COMMAND: Edit a PipoPal room name.
    '''
    args = message.content.split(' ')[2:]
    print(args)
    if len(args) < 1:
      await message.channel.send("{0}, specify a name. Ex: ppp name New Room!".format(message.author.mention))
      return
    new_name = args[0]
    print("New name: ",new_name)
    if not self.db.exists(message.channel.id):
      await message.channel.send("{0}, this isn't a PipoPal channel.".format(message.author.mention))
      return
    await message.channel.edit(name=new_name)
  async def cmd_create_room(self, message):
    '''
    COMMAND: Create a room with the mentioned users.
    '''
    if len(message.mentions) < 1:
      await message.channel.send("{0}, you need to specify a user. Ex: ppp create @User".format(message.author.mention))
      return
    if len(message.mentions) == 1 and message.mentions[0].id == message.author.id:
      await message.channel.send("{0}, you can't create a room with yourself.".format(message.author.mention))
      return
    guild = message.guild
    key = str(guild.id) + "::"
    users = [str(member.id) for member in message.mentions] + [str(message.author.id)]
    users.sort()
    key += ','.join(users)
    if self.db.exists(key) and self.get_channel(self.db.get(key)) is not None:
      error = "The room's already created."
      notify_error = ""
      print(error)
      await message.channel.send(error)
      await self.get_channel(self.db.get(key)).send(message.author.mention)
      return
    if self.db.exists(key) and self.db.exists(self.db.get(key)):
      self.db.delete(self.db.get(key))
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(read_messages=False),
      guild.me: discord.PermissionOverwrite(read_messages=True),
      message.author: discord.PermissionOverwrite(read_messages=False),
    }
    for member in message.mentions:
      overwrites[member] = discord.PermissionOverwrite(read_messages=True)
    channel = await guild.create_text_channel('PipoPal Room', overwrites=overwrites)
    self.db.store(key, channel.id)
    self.db.store(channel.id,'')

