'''fast rest api framework'''

__version__ = '0.0.3'


class __App:
    from .app import app


api = __App.app._Api
get = __App.app._get
post = __App.app._post
request = __App.app._request
response = __App.app._response
filter = __App.app._filter
R = __App.app._R
