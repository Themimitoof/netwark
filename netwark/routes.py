def includeme(config):
    config.add_static_view(name='static', path='../dist', cache_max_age=3600)
    config.add_route('overview', '/')
    config.add_route('operation_new', '/operation/new')
    config.add_route('operation_info', '/operation/{uuid}')
