from discord.ext import commands
from sqlalchemy.exc import OperationalError

from util.data.guild_data import GuildData


class Reactor(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="reactoradd", aliases=["Reactoradd"])
	@commands.has_permissions(manage_guild=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.guild_only()
	async def reactor_add(self, ctx, message_id: int, role_id: int, emoji: str):
		"""Add a reactor message."""
		await ctx.message.delete()

		if not ctx.guild.get_role(role_id):
			await ctx.send("Role not found!", delete_after=10)
			return

		GuildData(str(ctx.guild.id)).reactors.insert(message_id, role_id, emoji)

		await ctx.send('Reactor has been set.', delete_after=10)

		msg = await ctx.fetch_message(message_id)
		await msg.add_reaction(emoji)

	@commands.command(name="reactorget", aliases=["reactorlist", "Reactorget", "Reactorlist"])
	@commands.has_permissions(manage_guild=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.guild_only()
	async def reactor_get(self, ctx):
		"""Get the available reactors."""
		await ctx.message.delete()

		reactors = GuildData(str(ctx.guild.id)).reactors.fetch_all()

		if reactors:
			message = "\nReactors\n------------\nMessage ID - Role ID - Emoji\n\n"

			for r in reactors:
				message += f"{r[1]} - {r[2]} - {r[3]}\n"
			message += f"\nTotal Amount: {len(reactors)}\n"

			msg_parts = [(message[i:i + 1500]) for i in range(0, len(message), 1500)]

			for part in msg_parts:
				await ctx.send(f"```{part}```")
		else:
			await ctx.send('No reactors currently set!', delete_after=10)

	@commands.command(name="reactordelete", aliases=["reactorclear", "Reactordelete", "Reactorclear"])
	@commands.has_permissions(manage_guild=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.guild_only()
	async def reactor_delete(self, ctx, message_id: int):
		"""Delete all reactors on a specific message."""
		await ctx.message.delete()

		data_reactors = GuildData(str(ctx.guild.id)).reactors
		reactors = data_reactors.fetch_all()

		if reactors is None or len(reactors) == 0:
			await ctx.send("No reactors currently set!", delete_after=10)
			return

		result = data_reactors.delete(message_id)
		if result:
			await ctx.send("Reactors removed from message.", delete_after=10)
		else:
			await ctx.send("Reactor not found.", delete_after=10)

	@commands.command(name="reactorclearall", aliases=["reactordeleteall", "Reactorclearall", "Reactordeleteall"])
	@commands.has_permissions(manage_guild=True)
	@commands.cooldown(1, 2, commands.BucketType.user)
	@commands.guild_only()
	async def reactor_clear_all(self, ctx):
		"""Clear all reactors."""
		await ctx.message.delete()

		GuildData(str(ctx.guild.id)).reactors.delete_all()

		await ctx.send("All reactors deleted.")

	@commands.Cog.listener("on_raw_reaction_add")
	async def on_raw_reaction_add(self, payload):
		await self.reaction_handle(payload, add_mode=True)

	@commands.Cog.listener("on_raw_reaction_remove")
	async def on_raw_reaction_remove(self, payload):
		await self.reaction_handle(payload, add_mode=False)

	@commands.Cog.listener("on_raw_message_delete")
	async def on_raw_message_delete(self, payload):
		guild = self.bot.get_guild(payload.guild_id)

		try:
			reactors = GuildData(str(guild.id)).reactors
			if len(reactors.fetch_all()) <= 0:
				return

			reactors.delete(payload.message_id)
		except (OperationalError, NameError):
			print("Unable to load SQLAlchemy Database, skipping reactor check...")

	async def reaction_handle(self, payload, add_mode: bool):
		guild = self.bot.get_guild(payload.guild_id)
		user = payload.member if payload.member else await guild.fetch_member(payload.user_id)

		if user == self.bot.user:
			return

		reactors = GuildData(str(guild.id)).reactors.fetch_all()
		reactors_filtered = filter(lambda r: payload.message_id == r[1], reactors)
		list_reactors = list(reactors_filtered)

		if len(list_reactors) > 0:
			for reac in list_reactors:
				re_msg_id = reac[1]
				re_role_id = reac[2]
				re_emoji = reac[3]

				reaction_emoji = str(payload.emoji)
				if reaction_emoji == re_emoji:
					role = guild.get_role(re_role_id)
					if add_mode:
						await user.add_roles(role, reason=f"Reacted: {re_msg_id}")
						await user.send(f"**Role Added**\nYou have joined the *{role.name}* Team.")
					else:
						await user.remove_roles(role, reason=f"Un-Reacted: {re_msg_id}")
						await user.send(f"**Role Removed**\nYou have left the *{role.name}* Team.")


def setup(bot):
	bot.add_cog(Reactor(bot))
