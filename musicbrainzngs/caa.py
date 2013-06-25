import json

import compat
import musicbrainz

hostname = "coverartarchive.org"

def set_caa_hostname(new_hostname):
    """Set the base hostname for Cover Art Archive requests.
    Defaults to 'coverartarchive.org'."""
    global hostname
    hostname = new_hostname

def _caa_request(releaseid, imageid=None, size=None):
    """ Make a CAA request.
    imageid and size, if specified, must be strings.
    imageid should be 'front', 'back', or a number
    size must be 250 or 500
    """
    # Construct the full URL for the request, including hostname and
    # query string.
    path = ["release", releaseid]
    if imageid and size:
        path.append("%s-%s" % (imageid, size))
    elif imageid:
        path.append(imageid)
    url = compat.urlunparse((
        'http',
        hostname,
        '/%s' % '/'.join(path),
        '',
        '',
        ''
    ))
    musicbrainz._log.debug("GET request for %s" % (url, ))

    # Set up HTTP request handler and URL opener.
    httpHandler = compat.HTTPHandler(debuglevel=0)
    handlers = [httpHandler]

    opener = compat.build_opener(*handlers)

    # Make request.
    req = musicbrainz._MusicbrainzHttpRequest("GET", url, None)
    # Useragent isn't needed for CAA, but we'll add it if it exists
    if musicbrainz._useragent != "":
        req.add_header('User-Agent', musicbrainz._useragent)
        musicbrainz._log.debug("requesting with UA %s" % musicbrainz._useragent)

    resp = musicbrainz._safe_read(opener, req, None)

    # TODO: Could use response headers here
    if imageid:
        # If we asked for an image, return the image
        return resp
    else:
        # Otherwise it's json
        return json.loads(resp)

def get_coverart_list(releaseid):
    """ Get the list of coverart associated with a release.
    The format is the same as the json representation returned
    by the Cover Art Archive.

    If there is no coverart for this release then None is returned.

    If an error occurs then a musicbrainz.ResponseError will
    be raised with one of the following HTTP codes:
    400: Releaseid is not a UUID
    503: Ratelimit exceeded
    """
    try:
        return _caa_request(releaseid)
    except musicbrainz.ResponseError as e:
        if e.cause.code == 404:
            return None
        else:
            raise

def download_coverart_front(releaseid, size=None):
    """ Download the front coverart for a release.
    If `size' is not specified, download the largest copy present.
    `size' can be one of 250 or 500 (as an integer or a string)

    If there is no coverart for this release or if no front image
    has been chosen then None is returned.

    If an error occurs then a musicbrainz.ResponseError will
    be raised with one of the following HTTP codes:
    400: Releaseid is not a UUID
    503: Ratelimit exceeded
    """
    if isinstance(size, int):
        size = "%d" % (size, )
    try:
        return _caa_request(releaseid, "front", size=size)
    except musicbrainz.ResponseError as e:
        if e.cause.code == 404:
            return None
        else:
            raise

def download_coverart_back(releaseid, size=None):
    """ Download the back coverart for a release.
    If `size' is not specified, download the largest copy present.
    `size' can be one of 250 or 500 (as an integer or a string)

    If there is no coverart for this release or if no back image
    has been chosen then None is returned.

    If an error occurs then a musicbrainz.ResponseError will
    be raised with one of the following HTTP codes:
    400: Releaseid is not a UUID
    503: Ratelimit exceeded
    """
    if isinstance(size, int):
        size = "%d" % (size, )
    try:
        return _caa_request(releaseid, "back", size=size)
    except musicbrainz.ResponseError as e:
        if e.cause.code == 404:
            return None
        else:
            raise

def download_coverart(releaseid, coverid, size=None):
    """ Download coverart for a release. The coverart file to download
    is specified by the `coverid' argument.
    If `size' is not specified, download the largest copy present.
    `size' can be one of 250 or 500 (as an integer or a string)

    If there is no coverart for this release or if the given 
    coverid doesn't exist then None is returned.

    If an error occurs then a musicbrainz.ResponseError will
    be raised with one of the following HTTP codes:
    400: Releaseid is not a UUID
    503: Ratelimit exceeded
    """
    if isinstance(coverid, int):
        coverid = "%d" % (coverid, )
    if isinstance(size, int):
        size = "%d" % (size, )
    try:
        return _caa_request(releaseid, coverid, size=size)
    except musicbrainz.ResponseError as e:
        if e.cause.code == 404:
            return None
        else:
            raise
