def includeme(settings):
    settings.route_prefix = '/api/v1'
    settings.scan('.')
