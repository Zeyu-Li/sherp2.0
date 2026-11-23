import asyncio
import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace

import discord
import pytest
from discord.ext import commands

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_bot_messages_never_ping_anyone(monkeypatch):
    # /course prereq echoes the department the user typed, e.g. a role mention.
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr(commands.Bot, "run", lambda self, *args, **kwargs: None)
    bot = load_module("bot", "bot.py")

    assert bot.client.allowed_mentions.to_dict() == {"parse": []}


def test_sync_is_owner_only():
    from cogs.misc import Misc

    bot = commands.Bot(command_prefix="?", intents=discord.Intents.none(), owner_id=1)
    asyncio.run(bot.add_cog(Misc(bot)))
    sync = bot.get_command("sync")

    def ctx_for(user_id: int):
        return SimpleNamespace(
            interaction=None,
            bot=bot,
            author=SimpleNamespace(id=user_id),
            guild=None,
            command=sync,
            cog=bot.get_cog("Misc"),
        )

    with pytest.raises(commands.NotOwner):
        asyncio.run(sync.can_run(ctx_for(2)))
    assert asyncio.run(sync.can_run(ctx_for(1)))
