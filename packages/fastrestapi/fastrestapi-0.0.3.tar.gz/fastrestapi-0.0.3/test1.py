from fastrestapi import R, api, filter, get, post, request


@get("/test1")
def test1():
    print("test1")
    return R.data("测试1")


@post("/test2")
def test2():
    print("test2")
    return R.data("测试2")


@filter
def auth():
    print(f"@req {request.method} {request.path}")
    print("auth check")


if __name__ == '__main__':
    api.run("localhost", 5000)
