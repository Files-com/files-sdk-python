from files_sdk.api import Api


class ListObj:
    def __init__(self, klass, path, method, params, options):
        self.klass = klass
        self.path = path
        self.method = method
        self.params = params
        self.options = options
        self.data = []
        self.cursor = None

        self.load_next_page()

    def load_next_page(self):
        if self.cursor is not None:
            self.params["cursor"] = self.cursor
        response, _options = Api.send_request(
            self.path, self.method, self.params, self.options
        )
        self.data = [self.klass(d, self.options) for d in response.data]
        self.cursor = response.headers.get("X-Files-Cursor", None)
        return self

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def auto_paging_iter(self):
        while True:
            for item in self.data:
                yield item
            if not self.has_next_page:
                break
            self.load_next_page()

    @property
    def has_next_page(self):
        return True if self.cursor is not None else False
