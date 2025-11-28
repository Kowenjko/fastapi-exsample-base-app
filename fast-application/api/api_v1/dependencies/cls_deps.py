from typing import Annotated, Generator, Self
from fastapi import Header, Request


class PathReaderDependency:
    def __init__(self, source: str):
        self.source = source
        self._request: Request | None = None
        self._foobar: str = ""

    def as_dependency(
        self, request: Request, foobar: Annotated[str, Header(alias="x-foobar")] = "foo"
    ) -> Generator[Self, None, None]:
        self._request = request
        self._foobar = foobar
        yield self

        self._request = None
        # self._foobar = ""

    @property
    def path(self) -> str:
        if self._request is None:
            return ""
        return self._request.url.path

    def read(self, **kwargs: str) -> dict[str, str]:
        return {
            "source": self.source,
            "path": self.path,
            "kwargs": kwargs,
            "foobar": self._foobar,
        }


path_reader = PathReaderDependency(source="abc/path/foo/bar")
