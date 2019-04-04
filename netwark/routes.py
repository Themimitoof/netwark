def includeme(config):
    config.add_static_view(name='static', path='../dist', cache_max_age=3600)

    #  General routes
    config.add_route('overview', '/')

    # Operations related routes
    config.add_route('operation_new', '/operation/new')
    config.add_route('operation_info', '/operation/{uuid}')

    # IP Calc routes
    config.add_route('ipcalc', '/ipcalc')

    # WHOIS routes
    config.add_route('whois_main', '/whois')
    config.add_route('whois_resource', '/whois/{resource}')

    # MAC OUI routes
    config.add_route('mac_oui', '/mac-oui')
