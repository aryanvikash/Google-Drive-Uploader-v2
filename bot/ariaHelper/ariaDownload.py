# File from Public leech repo


async def add_url(aria_instance, text_url, c_file_name):
    options = None

    uris = [text_url]
    # Add URL Into Queue
    try:
        download = aria_instance.add_uris(
            uris,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e)
    else:
        return download.gid


async def add_torrent(aria_instance, text_url, c_file_name):
    options = None

    magnet = text_url
    # Add URL Into Queue
    try:
        download = aria_instance.add_magnet(
            magnet,
            {'dir': c_file_name}
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e)
    else:
        return download.gid
