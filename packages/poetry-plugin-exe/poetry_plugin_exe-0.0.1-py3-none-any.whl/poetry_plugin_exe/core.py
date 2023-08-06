#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
<TBD>

:date:      2022
:author:    Christian Wiche
:contact:   cwichel@gmail.com
:license:   The MIT License (MIT)
"""
# -------------------------------------

import typing as tp

from cleo.helpers import argument
from poetry.console.application import Application
from poetry.console.commands.env_command import EnvCommand
from poetry.plugins.application_plugin import ApplicationPlugin


# -->> Tunables <<---------------------


# -->> Definitions <<------------------


# -->> API <<--------------------------
class PoetryPluginExeCommand(EnvCommand):
    name = "exe"
    description = "Execute commands from your pyproject.toml"
    arguments = [
        argument(name="cmd", description="Command to execute", multiple=False),
        argument(name="args", description="Arguments to append to the command", multiple=True, optional=True),
    ]

    def handle(self) -> int:
        print("Hello!")
        return 0

    @classmethod
    def factory(cls) -> "PoetryPluginExeCommand":
        return cls()


class PoetryPluginExe(ApplicationPlugin):
    def activate(self, application: Application, *args: tp.Any, **kwargs: tp.Any) -> None:
        application.command_loader.register_factory(command_name="exe", factory=PoetryPluginExeCommand.factory)


# -->> Export <<-----------------------
__all__ = [
    "PoetryPluginExe",
]
