from __future__ import annotations

from random import choice
from typing import Union

from discord import Embed
from discord.ext.commands import Bot, Context


class Card:
    def __init__(self, text: str, count: int = 1):
        self.text = text
        self.count = count

    @staticmethod
    def load(card: dict) -> Union[dict, Card]:
        if "text" in card:
            return Card(**card)
        else:
            return card

    def display(self) -> str:
        text = self.text.replace("_", "\\_").replace("'", "’")
        if self.count == 2:
            text += "\n\nPICK :two:"
        elif self.count == 3:
            text += "\n\nDRAW :two:\nPICK :three:"
        return f"**{text}**"


def main(*, cards, token: str, channel: int):
    bot = Bot("cah ")

    @bot.command()
    async def start(ctx: Context):
        if ctx.author.voice and ctx.author.voice.channel.id == channel:
            if len(ctx.author.voice.channel.members) > 2:
                await ctx.send("ded")
            else:
                await ctx.send(embed=Embed(description="This bot requires at least 3 players to play the game. If you "
                                                       "want to try a single player version of Cards Against Humanity, "
                                                       "visit the [Cards Against Humanity "
                                                       "Lab](https://lab.cardsagainsthumanity.com).", color=0))
        else:
            await ctx.send(embed=Embed(description=f"You have to be in the game voice channel (<#{channel}>) to start "
                                                   f"a game!", color=0))

    @bot.command()
    async def black(ctx: Context):
        card = cards["cards"]["black"][choice(cards["decks"]["black_nsfw" if ctx.channel.is_nsfw() else "black"])]
        await ctx.send(embed=Embed(description=card.display(), color=0))

    @bot.command()
    async def white(ctx: Context):
        card = cards["cards"]["white"][choice(cards["decks"]["white_nsfw" if ctx.channel.is_nsfw() else "white"])]
        await ctx.send(embed=Embed(description=card.display(), color=0xFFFFFF))

    bot.run(token)


if __name__ == '__main__':
    from json import load

    with open("config.json") as config:
        config = load(config)

    with open("cards.json") as cards:
        cards = load(cards, object_hook=Card.load)

    main(cards=cards, **config)
