from django.conf.urls import url
from django.conf import settings


def generate_url(regex, view, name=None):
    """
    This function only adds Api version to each regex (url).
    Returns base django url function with a new generated regex.
    :param regex: str
    :param view: view object
    :param name: str name of url (optional)
    :return: django.conf.urls.url object
    """

    regex = r"^" + settings.API_VERSION_URL + regex
    return url(regex, view, name=name)
