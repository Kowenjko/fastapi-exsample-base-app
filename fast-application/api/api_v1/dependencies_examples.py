from typing import Annotated

from fastapi import APIRouter, Depends, Header

from .dependencies.func_deps import (
    get_great_helper,
    get_x_foo_bar,
    get_header_dependency,
)
from utils.helper import GreatHelper, GreatService

from .dependencies.cls_deps import (
    path_reader,
    PathReaderDependency,
    TokenIntrospectResult,
    access_required,
    HeaderAccessDependency,
)


router = APIRouter(tags=["Dependencies Examples"])


@router.get("/single-direct-dependency")
def single_direct_dependency(foobar: Annotated[str, Header()]):
    return {"foobar": foobar, "message": "This is a single direct dependency example."}


@router.get("/single-via-func")
def single_via_func(foobar: Annotated[str, Depends(get_x_foo_bar)]):
    return {
        "x-foobar": foobar,
        "message": "This is a single dependency via function example.",
    }


@router.get("/multiple-dependencies")
def multiple_dependencies(
    foobar: Annotated[str, Header()],
    foobar_via_func: Annotated[str, Depends(get_x_foo_bar)],
):
    return {
        "foobar": foobar,
        "foobar_via_func": foobar_via_func,
        "message": "This is a multiple dependencies example.",
    }


@router.get("/multi-indirect")
def multi_indirect_dependencies(
    foobar: Annotated[str, Depends(get_header_dependency("x-foobar"))],
    foobar_via_func: Annotated[
        str,
        Depends(
            get_header_dependency(header_name="x-fizz-buzz", default_value="FizzBuzz")
        ),
    ],
):
    return {
        "foobar": foobar,
        "foobar_via_func": foobar_via_func,
        "message": "This is a multiple.",
    }


@router.get("/top-level-helper-creation")
def top_level_helper_creation(
    helper_name: Annotated[
        str,
        Depends(
            get_header_dependency(
                header_name="x-helper-name", default_value="HelperName"
            )
        ),
    ],
    helper_default: Annotated[
        str,
        Depends(get_header_dependency("x-helper-default")),
    ],
):
    helper = GreatHelper(name=helper_name, default=helper_default)

    return {
        "helper": helper.as_dict(),
        "message": "This is a top-level helper creation example.",
    }


@router.get("/helper-as-dependency")
def helper_as_dependency(helper: Annotated[GreatHelper, Depends(get_great_helper)]):
    return {
        "helper": helper.as_dict(),
        "message": "This is a top-level helper creation example.",
    }


@router.get("/great-service-as-dependency")
def great_service_as_dependency(
    service: Annotated[GreatService, Depends(GreatService)],
):
    return {
        "service": service.as_dict(),
        "message": "This is a great service as dependency example.",
    }


@router.get("/path-reader-dependency-from-method")
def path_reader_dependency_from_method(
    reader: Annotated[
        PathReaderDependency,
        Depends(path_reader.as_dependency),
        # Depends(PathReaderDependency(source="direct/bar").as_dependency),
    ],
):
    return {
        "read_result": reader.read(foo="bar"),
        "message": "This is a path reader dependency from method example.",
    }


@router.get("/direct-cls-dependency")
def direct_cls_dependency(
    token_data: Annotated[
        TokenIntrospectResult,
        # Depends(access_required),
        Depends(HeaderAccessDependency(secret_token="new_token")),
    ],
):
    return {
        "token_data": token_data.model_dump(),
        "message": "This is a direct class-based dependency example.",
    }
