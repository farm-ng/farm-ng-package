from typing import Optional, List
from pathlib import Path

from setuptools import Command
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install

from farm_ng.package.package import (
    build_package_protos,
    clean_protos,
)


def find_command(command_set: List[tuple], command_target: str) -> Optional[str]:
    for command, _, command_value in command_set:
        if command == command_target:
            return command_value
    return None


class BuildProtosCommand(Command):
    user_options = []  # type: ignore

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        proto_root: Optional[str] = find_command(self.user_options, "proto-root=")
        assert proto_root is not None

        package_root: Optional[str] = find_command(self.user_options, "package-root=")
        assert package_root is not None

        build_package_protos(
            proto_root=Path(proto_root), package_root=Path(package_root)
        )


class CleanFilesCommand(Command):
    user_options = []  # type: ignore

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        package_root: Optional[str] = find_command(self.user_options, "package-root=")
        assert package_root is not None

        clean_protos(package_root=Path(package_root))


class BuildProtosInstall(install):
    def run(self):
        # 1. Build the protobufs
        BuildProtosCommand.run(self)
        # 2. Run the installation
        install.run(self)
        # 3. Clean the generated protobufs
        CleanFilesCommand.run(self)


class BuildProtosDevelop(develop):
    def run(self):
        # 1. Build the protobufs
        BuildProtosCommand.run(self)
        # 2. Run the installation
        develop.run(self)


class BuildProtosEggInfo(egg_info):
    def run(self):
        # 1. Build the protobufs
        BuildProtosCommand.run(self)
        # 2. Run the installation
        egg_info.run(self)
