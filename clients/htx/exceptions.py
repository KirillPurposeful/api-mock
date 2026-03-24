class HtxAPIError(Exception):

    def __init__(self, err_code: str, err_msg: str) -> None:
        super().__init__(f"{err_code}: {err_msg}")
        self.err_code = err_code
        self.err_msg = err_msg