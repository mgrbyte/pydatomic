# Python2 compatability handled in exception cases.
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin  # noqa
