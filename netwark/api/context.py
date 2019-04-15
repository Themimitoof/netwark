"""
The Root Context

used when a view did not declare it's own context.
"""

from pyramid.security import (Everyone, Authenticated, Allow,
                              NO_PERMISSION_REQUIRED, ALL_PERMISSIONS,
                              )


class APIContext(object):
    """
    A default request context.
    """
    default_acl = [
        (Allow, Everyone, NO_PERMISSION_REQUIRED),
        (Allow, Authenticated, ['authenticated']),
        (Allow, 'god', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request
