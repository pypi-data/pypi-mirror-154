"""
Posix File gatherer
"""

import logging
import pathlib
from typing import Optional
from collections.abc import Iterable, Sequence

from more_itertools import pairwise
from ready_set_deploy.components import Component
from ready_set_deploy.elements import Atom, List

from ready_set_deploy.gatherers.base import Gatherer

log = logging.getLogger(__name__)


class PosixFileGatherer(Gatherer):
    NAME = "file.posix"

    def empty(self) -> Component:
        return Component(
            name=self.NAME,
            elements={
                "path": Atom.zero(),
                "owner": Atom.zero(),
                "group": Atom.zero(),
                "permissions": Atom.zero(),
                "contents": List.zero(),
            },
        )

    def gather_local(self, *, qualifier: tuple[str, ...] = ()) -> Component:
        # qualifier is the path segments leading to the file
        parts = self._to_absolute_parents(qualifier)

        return Component(
            name=self.NAME,
            qualifier=qualifier,
            elements={
                "path": Atom(""),
                "owner": Atom.zero(),
                "group": Atom.zero(),
                "permissions": Atom.zero(),
                "contents": List.zero(),
            },
        )


class TextFileContentsProvider(Provider):
    PROVIDER_NAME = "file.text"

    def gather_local(self, *, qualifier: Optional[str] = None, previous_state: Optional[SubsystemState] = None) -> SubsystemState:
        if qualifier is None:
            raise ValueError("qualifier must be specified")

        # break up the qualifier into component parts
        path = pathlib.Path(qualifier)
        parts = self._to_absolute_parents(path)

        state_parts = [self._gather_part(chunk, recursive=False) for chunk in parts[:-1]]
        state_parts.append(self._gather_part(parts[-1], recursive=True))
        for parent, child in pairwise(state_parts):
            parent["contents"] = [child]

        return SubsystemState(
            name=self.PROVIDER_NAME,
            qualifier=parts[0].anchor,
            state_type=SubsystemStateType.DESIRED,
            elements=[state_parts[0]],
        )

    def _to_absolute_parents(self, path: pathlib.Path) -> list[pathlib.Path]:
        if not path.is_absolute():
            path = pathlib.Path.cwd().joinpath(path)

        parts = path.parts
        current = pathlib.Path(parts[0])
        result = []
        for part in parts[1:]:
            if part == "..":
                result.pop()
                current = current.parent
            elif part == ".":
                continue
            else:
                current = current.joinpath(part)
                result.append(current)

        return result

    def _gather_part(self, path: pathlib.Path, *, recursive: bool = True) -> dict:
        if path.is_symlink():
            file_state = {
                "type": "symlink",
                "contents": path.readlink(),
                "partial": False,
            }
        elif path.is_dir():
            file_state = {
                "type": "directory",
                "contents": [],
                "partial": True,
            }
            if recursive:
                log.debug("recursively gathering from %s", path)
                file_state["contents"] = [self._gather_part(child, recursive=recursive) for child in path.iterdir()]
                file_state["partial"] = False
        elif path.is_file():
            log.debug("gathering %s contents", path)
            with open(path) as f:
                contents = f.readlines()

            file_state = {
                "type": "file",
                "contents": contents,
                "partial": False,
            }
        else:
            file_state = {
                "type": "missing",
                "contents": [],
                "partial": False,
            }

        file_state["name"] = path.name

        return file_state

    def diff(self, actual: SubsystemState, goal: SubsystemState) -> tuple[SubsystemState, SubsystemState]:
        # only actually defined between full and full - but full has different meaning for this provider
        assert actual.qualifier == goal.qualifier

        desired = SubsystemState(
            name=self.PROVIDER_NAME,
            qualifier=actual.qualifier,
            state_type=SubsystemStateType.DESIRED,
            elements=[],
        )
        undesired = SubsystemState(
            name=self.PROVIDER_NAME,
            qualifier=actual.qualifier,
            state_type=SubsystemStateType.UNDESIRED,
            elements=[],
        )
        return desired, undesired

    def to_commands(self, desired: Optional[SubsystemState], undesired: Optional[SubsystemState]) -> Iterable[Sequence[str]]:
        return []

    def is_valid(self, state: SubsystemState) -> Iterable[str]:
        # Once full, all children must be full

        return []


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    p = TextFileContentsProvider()
    state = p.gather_local(qualifier="../../scripts")
    import json
    from ready_set_deploy.model import DataclassEncoder

    print(json.dumps(state, cls=DataclassEncoder, indent=2))
    # print(state)
