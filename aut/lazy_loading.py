"""
A command group which lazily loads its subcommands.

Source:
https://click.palletsprojects.com/en/8.1.x/complex/#defining-the-lazy-group
"""

import importlib
from typing import Any

import click


MODULE_NAME_PREFIX = "aut.commands."


class LazyGroup(click.Group):
    lazy_subcommands: dict[str, str]

    def __init__(
        self, lazy_subcommands: dict[str, str], *args: Any, **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.lazy_subcommands = lazy_subcommands

    def list_commands(self, ctx: click.Context) -> list[str]:
        base_commands = super().list_commands(ctx)
        lazy_commands = sorted(self.lazy_subcommands.keys())
        return base_commands + lazy_commands

    def get_command(
        self, ctx: click.Context, cmd_name: str
    ) -> click.Command | None:
        if cmd_name in self.lazy_subcommands:
            return self._lazy_load(cmd_name)
        return super().get_command(ctx, cmd_name)

    def _lazy_load(self, cmd_name: str) -> click.Command:
        import_path = self.lazy_subcommands[cmd_name]
        module_name, cmd_object_name = import_path.rsplit(".", 1)
        module = importlib.import_module(MODULE_NAME_PREFIX + module_name)

        cmd_object = getattr(module, cmd_object_name)
        if not isinstance(cmd_object, click.Command):
            raise ValueError(
                f"Lazy loading of {import_path} failed by returning "
                "a non-command object"
            )
        return cmd_object
