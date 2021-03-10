from disco.bot import Plugin
from disco.types.interaction import InteractionType, InteractionResponseType


class SlashCommandPlugin(Plugin):
    @Plugin.listen('InteractionCreate')
    def on_interaction(self, event):
        if event.type == InteractionType.APPLICATION_COMMAND:
            event.interaction.create_response(InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE, {
                'content': 'It works!',
            })
