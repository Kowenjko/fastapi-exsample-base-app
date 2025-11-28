from typing import Annotated, Generator, Self
from fastapi import HTTPException, Header, Request, status
from pydantic import BaseModel


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


class TokenData(BaseModel):
    id: int
    username: str


class TokenIntrospectResult(BaseModel):
    result: TokenData


class HeaderAccessDependency:

    def __init__(self, secret_token: str):
        self.secret_token = secret_token

    def validate(self, token: str) -> None:
        if token != self.secret_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token {token} invalid token",
            )
        return TokenIntrospectResult(result=TokenData(id=1, username="test_user"))

    def __call__(
        self, token: Annotated[str, Header(alias="x-secret-token")]
    ) -> TokenIntrospectResult:
        token_data = self.validate(token=token)
        # log.info("Token validated successfully")
        return token_data


access_required = HeaderAccessDependency(secret_token="supersecret_token")
