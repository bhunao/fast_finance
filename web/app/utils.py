from fastapi import Request


def is_hx_request(request: Request):
    return request.headers.get("Hx-Request") == "true"
