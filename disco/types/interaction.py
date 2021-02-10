from holster.enum import Enum

from disco.types.base import (
    SlottedModel, Field, ListField, snowflake
)
from disco.types.guild import GuildMember


InteractionType = Enum(
    PING=1,
    APPLICATION_COMMAND=2,
)

InteractionResponseType = Enum(
    PONG=1,
    ACKNOWLEDGE=2,
    CHANNEL_MESSAGE=3,
    CHANNEL_MESSAGE_WITH_SOURCE=4,
    ACKNOWLEDGE_WITH_SOURCE=5,
)

ApplicationCommandOptionType = Enum(
    SUB_COMMAND=1,
    SUB_COMMAND_GROUP=2,
    STRING=3,
    INTEGER=4,
    BOOLEAN=5,
    USER=6,
    CHANNEL=7,
    ROLE=8,
)


class ApplicationCommandInteractionDataOption(SlottedModel):
    name = Field(str)
    value = Field(ApplicationCommandOptionType)
    options = ListField('ApplicationCommandInteractionDataOption')


class ApplicationCommandInteractionData(SlottedModel):
    id = Field(snowflake)
    name = Field(str)
    options = ListField(ApplicationCommandInteractionDataOption)


class Interaction(SlottedModel):
    id = Field(snowflake)
    type = Field(InteractionType)
    data = Field(ApplicationCommandInteractionData)
    guild_id = Field(snowflake)
    channel_id = Field(snowflake)
    member = Field(GuildMember)
    token = Field(str)
    version = Field(int)

    def create_response(self, interaction_response_type, data):
        from disco.api.client import APIClient
        if self.client is None:
            self.client = APIClient(None)
        self.client.api.interactions_create_response(self.id, self.token, interaction_response_type, data)
