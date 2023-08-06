from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.paginated_task_list import PaginatedTaskList
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    passive: Union[Unset, None, bool] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tasks/".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["description"] = description

    params["limit"] = limit

    params["name"] = name

    params["offset"] = offset

    params["ordering"] = ordering

    params["passive"] = passive

    params["run_environment__uuid"] = run_environment_uuid

    params["search"] = search

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[PaginatedTaskList]:
    if response.status_code == 200:
        response_200 = PaginatedTaskList.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PaginatedTaskList]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    passive: Union[Unset, None, bool] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedTaskList]:
    """
    Args:
        description (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        passive (Union[Unset, None, bool]):
        run_environment_uuid (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedTaskList]
    """

    kwargs = _get_kwargs(
        client=client,
        description=description,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        passive=passive,
        run_environment_uuid=run_environment_uuid,
        search=search,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    passive: Union[Unset, None, bool] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedTaskList]:
    """
    Args:
        description (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        passive (Union[Unset, None, bool]):
        run_environment_uuid (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedTaskList]
    """

    return sync_detailed(
        client=client,
        description=description,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        passive=passive,
        run_environment_uuid=run_environment_uuid,
        search=search,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    passive: Union[Unset, None, bool] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Response[PaginatedTaskList]:
    """
    Args:
        description (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        passive (Union[Unset, None, bool]):
        run_environment_uuid (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedTaskList]
    """

    kwargs = _get_kwargs(
        client=client,
        description=description,
        limit=limit,
        name=name,
        offset=offset,
        ordering=ordering,
        passive=passive,
        run_environment_uuid=run_environment_uuid,
        search=search,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    description: Union[Unset, None, str] = UNSET,
    limit: Union[Unset, None, int] = UNSET,
    name: Union[Unset, None, str] = UNSET,
    offset: Union[Unset, None, int] = UNSET,
    ordering: Union[Unset, None, str] = UNSET,
    passive: Union[Unset, None, bool] = UNSET,
    run_environment_uuid: Union[Unset, None, str] = UNSET,
    search: Union[Unset, None, str] = UNSET,
) -> Optional[PaginatedTaskList]:
    """
    Args:
        description (Union[Unset, None, str]):
        limit (Union[Unset, None, int]):
        name (Union[Unset, None, str]):
        offset (Union[Unset, None, int]):
        ordering (Union[Unset, None, str]):
        passive (Union[Unset, None, bool]):
        run_environment_uuid (Union[Unset, None, str]):
        search (Union[Unset, None, str]):

    Returns:
        Response[PaginatedTaskList]
    """

    return (
        await asyncio_detailed(
            client=client,
            description=description,
            limit=limit,
            name=name,
            offset=offset,
            ordering=ordering,
            passive=passive,
            run_environment_uuid=run_environment_uuid,
            search=search,
        )
    ).parsed
