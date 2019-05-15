def includeme(config):
    config.add_static_view(name='static', path='../dist', cache_max_age=3600)

    #  General routes
    config.add_route('overview', '/')

    # Operations related routes
    config.add_route('operations_list', '/operations')
    config.add_route('operations_info', '/operations/{uuid}')

    # IP Calc routes
    config.add_route('ipcalc', '/tools/ipcalc')

    # WHOIS routes
    config.add_route('whois_main', '/tools/whois')
    config.add_route('whois_resource', '/tools/whois/{resource}')

    # MAC OUI routes
    config.add_route('mac_oui', '/tools/mac-oui')
