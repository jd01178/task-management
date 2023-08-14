from .base import * # noqa
if DEBUG:
    from .development import * # noqa
else:
    from .production import * # noqa
