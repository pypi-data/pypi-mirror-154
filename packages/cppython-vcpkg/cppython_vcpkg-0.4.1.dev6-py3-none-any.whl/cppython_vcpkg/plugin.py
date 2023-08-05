"""
TODO
"""
import json
import subprocess
from os import name as system_name
from pathlib import Path, PosixPath, WindowsPath
from typing import Optional, Type

from cppython_core.schema import (
    PEP621,
    ConfigurePreset,
    CPPythonData,
    CPPythonModel,
    Generator,
    GeneratorConfiguration,
    GeneratorData,
)
from cppython_core.utility import subprocess_call
from pydantic import Field, HttpUrl


class VcpkgData(GeneratorData):
    """
    TODO
    """

    # TODO: Make relative to CPPython:build_path
    install_path: Path = Field(
        default=Path("build"),
        alias="install-path",
        description="The referenced dependencies defined by the local vcpkg.json manifest file",
    )

    manifest_path: Path = Field(
        default=Path(), alias="manifest-path", description="The directory to store the manifest file, vcpkg.json"
    )


class VcpkgDependency(CPPythonModel):
    """
    Vcpkg dependency type
    """

    name: str


class Manifest(CPPythonModel):
    """
    The manifest schema
    """

    name: str

    # TODO: Support other version types
    version: str
    homepage: Optional[HttpUrl] = Field(default=None)
    dependencies: list[VcpkgDependency] = Field(default=[])


class VcpkgGenerator(Generator[VcpkgData]):
    """
    _summary_

    Arguments:
        Generator {_type_} -- _description_
    """

    def __init__(
        self, configuration: GeneratorConfiguration, project: PEP621, cppython: CPPythonData, generator: VcpkgData
    ) -> None:
        """
        TODO
        """

        # Modify the vcpkg settings before sending it the base class to resolve dynamic modifications

        modified_generator = generator.copy(deep=True)

        # Resolve relative paths

        if not modified_generator.install_path.is_absolute():
            modified_generator.install_path = configuration.root_path.absolute() / modified_generator.install_path

        if not modified_generator.manifest_path.is_absolute():
            modified_generator.manifest_path = configuration.root_path.absolute() / modified_generator.manifest_path

        super().__init__(configuration, project, cppython, modified_generator)

    def _update_generator(self, path: Path):

        # TODO: Identify why Shell is needed and refactor
        try:
            if system_name == "nt":
                subprocess_call([str(WindowsPath("bootstrap-vcpkg.bat"))], cwd=path, shell=True)
            elif system_name == "posix":
                subprocess_call(["sh", str(PosixPath("bootstrap-vcpkg.sh"))], cwd=path, shell=True)
        except subprocess.CalledProcessError:
            self.logger.error("Unable to bootstrap the vcpkg repository", exc_info=True)
            raise

    def _extract_manifest(self) -> Manifest:
        """
        TODO
        """
        base_dependencies = self.cppython.dependencies

        vcpkg_dependencies: list[VcpkgDependency] = []
        for dependency in base_dependencies:
            vcpkg_dependency = VcpkgDependency(name=dependency.name)
            vcpkg_dependencies.append(vcpkg_dependency)

        # Create the manifest

        # Version is known to not be None, and has been filled
        # TODO: Type for ResolvedProject
        version = self.project.version
        assert version is not None

        return Manifest(name=self.project.name, version=version, dependencies=vcpkg_dependencies)

    @staticmethod
    def name() -> str:
        return "vcpkg"

    @staticmethod
    def data_type() -> Type[VcpkgData]:
        return VcpkgData

    def generator_downloaded(self, path: Path) -> bool:

        try:
            # Hide output, given an error output is a logic conditional
            subprocess_call(
                ["git", "rev-parse", "--is-inside-work-tree"],
                suppress=True,
                cwd=path,
            )

        except subprocess.CalledProcessError:
            return False

        return True

    def download_generator(self, path: Path) -> None:

        try:
            # The entire history is need for vcpkg 'baseline' information
            subprocess_call(
                ["git", "clone", "https://github.com/microsoft/vcpkg", "."],
                cwd=path,
            )

        except subprocess.CalledProcessError:
            self.logger.error("Unable to clone the vcpkg repository", exc_info=True)
            raise

        self._update_generator(path)

    def update_generator(self, path: Path) -> None:
        try:
            # The entire history is need for vcpkg 'baseline' information
            subprocess_call(["git", "fetch", "origin"], cwd=path)
            subprocess_call(["git", "pull"], cwd=path)
        except subprocess.CalledProcessError:
            self.logger.error("Unable to update the vcpkg repository", exc_info=True)
            raise

        self._update_generator(path)

    def install(self) -> None:
        """
        TODO
        """
        manifest_path = self.generator.manifest_path
        manifest = self._extract_manifest()

        # Write out the manifest
        serialized = json.loads(manifest.json(exclude_none=True))
        with open(manifest_path / "vcpkg.json", "w", encoding="utf8") as file:
            json.dump(serialized, file, ensure_ascii=False, indent=4)

        vcpkg_path = self.cppython.install_path / self.name()

        executable = vcpkg_path / "vcpkg"

        try:
            subprocess_call(
                [
                    executable,
                    "install",
                    f"--x-install-root={self.generator.install_path}",
                    f"--x-manifest-root={self.generator.manifest_path}",
                ],
                cwd=self.cppython.build_path,
            )
        except subprocess.CalledProcessError:
            self.logger.error("Unable to install project dependencies", exc_info=True)
            raise

    def update(self) -> None:
        """
        TODO
        """
        manifest_path = self.generator.manifest_path
        manifest = self._extract_manifest()

        # Write out the manifest
        serialized = json.loads(manifest.json(exclude_none=True))
        with open(manifest_path / "vcpkg.json", "w", encoding="utf8") as file:
            json.dump(serialized, file, ensure_ascii=False, indent=4)

        vcpkg_path = self.cppython.install_path / self.name()

        executable = vcpkg_path / "vcpkg"

        try:
            subprocess_call(
                [
                    executable,
                    "upgrade",
                    f"--x-install-root={self.generator.install_path}",
                    f"--x-manifest-root={self.generator.manifest_path}",
                ],
                cwd=self.cppython.build_path,
            )
        except subprocess.CalledProcessError:
            self.logger.error("Unable to install project dependencies", exc_info=True)
            raise

    def generate_cmake_config(self) -> ConfigurePreset:

        toolchain_file = self.cppython.install_path / self.name() / "scripts/buildsystems/vcpkg.cmake"

        configure_preset = ConfigurePreset(name=self.name(), toolchainFile=str(toolchain_file))

        return configure_preset
