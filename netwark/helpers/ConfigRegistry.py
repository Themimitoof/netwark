class ConfigRegistry:
    """
    Store the configuration of the specified app in argument.
    """

    _conf = {}

    def __init__(self, app, config=None):
        if 'app' not in self._conf:
            self.app = app

            if config:
                self._conf[app] = config

    def __repr__(self):
        return "<ConfigRegistry - app %r @ %s>" % (self.app, id(self))

    @property
    def configuration(self):
        return self._conf[self.app]
