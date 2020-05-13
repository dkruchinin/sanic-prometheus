def get_from_url(request, lim=0):
    if lim <= 0:
        return request.path
    url = request.path
    if url[0] == '/':
        lim += 1
    return '/'.join(url.split('/')[:lim])


def make_url_endpoint_fn(url_type):
    lim_str = url_type[4:]
    if not lim_str:
        return get_from_url
    else:
        try:
            n = int(lim_str)
        except ValueError:
            raise ValueError(
                'url endpoint type can be either "url" or "url:<int>"'
            )
        return lambda req: get_from_url(req, lim=n)


def fn_by_type(ep_type, get_endpoint_fn):
    if ep_type.startswith('url'):
        return make_url_endpoint_fn(ep_type)
    elif ep_type == 'custom':
        if get_endpoint_fn is None:
            raise ValueError(
                '"custom" type requires endpoint function to be set'
            )
        return get_endpoint_fn
    else:
        raise ValueError('Unsupported endpoint type "{}"'.format(ep_type))


__all__ = ['fn_by_type', 'get_from_url']
