from holster.enum import Enum

from disco.api.client import APIClient
from disco.types.base import (
    SlottedModel, Field, ListField, snowflake, cached_property
)
from disco.types.guild import GuildMember


InteractionType = Enum(
    PING=1,
    APPLICATION_COMMAND=2,
)

InteractionResponseType = Enum(
    PONG=1,
    CHANNEL_MESSAGE_WITH_SOURCE=4,
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE=5,
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

    def __init__(self):
        if self.client is None:
            self.client = APIClient(None)

    @cached_property
    def application_id(self):
        resp = self.client.api.oauth_applications_me()
        return resp['id']

    def create_response(self, interaction_response_type, data):
        self.client.api.interactions_create_response(self.id, self.token, interaction_response_type, data)

    def edit_response(self, content=None, embeds=None, allowed_mentions=None):
        self.client.api.interactions_edit_response(self.id, self.token, content, embeds, allowed_mentions)

    def delete_response(self):
        self.client.api.interactions_delete_response(self.id, self.token)

    def create_followup(
        self,
        content=None,
        embeds=None,
        username=None,
        avatar_url=None,
        tts=None,
        file_content=None,
        allowed_mentions=None
    ):
        self.client.api.interactions_create_followup(
            self.application_id,
            self.token,
            content,
            embeds,
            username,
            avatar_url,
            tts,
            file_content,
            allowed_mentions
        )

    def edit_followup(
        self,
        message,
        content=None,
        embeds=None,
        allowed_mentions=None
    ):
        self.client.api.interactions_edit_followup(
            self.application_id,
            message.id,
            self.token,
            content,
            embeds,
            allowed_mentions
        )

    def delete_followup(self, message):
        self.client.api.interactions_delete_followup(self.application_id, message.id, self.token)
