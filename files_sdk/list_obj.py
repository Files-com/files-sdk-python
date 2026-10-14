from typing import Any, Generic, Iterator, TypeVar

from files_sdk.api import LEGACY, Operation
from files_sdk.error import APIConnectionError

T = TypeVar("T")


class ListObj(Generic[T]):
    """One page of a cursor-paginated list.

    Iterating a ListObj yields the records on the current page.
    auto_paging_iter() yields every record from the current page onward,
    fetching each later page only when the caller asks for more.

    The later pages come from the same client and settings as the first,
    and share its operation's deadline and cancellation token. The current
    page stays readable after that operation stops or its client closes;
    fetching another page then raises.
    """

    def __init__(
        self,
        klass: type[T],
        method: str,
        path: str,
        params: Any,
        options: Any = None,
    ):
        self.klass = klass
        self.method = method
        self.path = path
        self._operation = (
            options
            if isinstance(options, Operation)
            else Operation.start(LEGACY, options)
        )
        # Copies, so advancing never writes a cursor into the caller's
        # dictionaries and later edits to them cannot change this list.
        self.params = dict(params)
        self.options = dict(self._operation.options)
        self.data: list[T] = []
        self.cursor: str | None = None
        self._fetched_cursors: set[str | None] = set()

        self._load_page(self.params.get("cursor"))

    def load_next_page(self) -> "ListObj[T]":
        if self.has_next_page:
            self._load_page(self.cursor)
        return self

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def auto_paging_iter(self) -> Iterator[T]:
        while True:
            yield from self.data
            if not self.has_next_page:
                return
            self.load_next_page()

    @property
    def has_next_page(self) -> bool:
        return self.cursor is not None

    def _load_page(self, cursor):
        if cursor in self._fetched_cursors:
            raise APIConnectionError(
                "Files.com returned a pagination cursor that this list has "
                "already followed. Stopping instead of fetching the same "
                "records again."
            )

        params = dict(self.params)
        if cursor is not None:
            params["cursor"] = cursor
        response = self._operation.request(self.method, self.path, params)
        page = self._operation.decode_models(response, self.klass)

        # Publish the page only after it is fully built, so a failed request
        # or an unreadable page leaves the current page and cursor in place
        # for a retry.
        self._fetched_cursors.add(cursor)
        self.data = page
        # Files.com names the next page's cursor in X-Files-Cursor-Next. An
        # answer without that header may name it in X-Files-Cursor, as the
        # API has long done. A missing or blank cursor marks the last page.
        cursor = response.headers.get("X-Files-Cursor-Next")
        if cursor is None:
            cursor = response.headers.get("X-Files-Cursor")
        self.cursor = cursor or None
