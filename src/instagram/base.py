#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Instagram API
# Copyright (c) 2008-2016 Hive Solutions Lda.
#
# This file is part of Hive Instagram API.
#
# Hive Instagram API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Instagram API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Instagram API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2016 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import tag
from . import user
from . import media
from . import subscription

BASE_URL = "https://api.instagram.com/"
""" The default base url to be used when no other
base url value is provided to the constructor """

CLIENT_ID = None
""" The default value to be used for the client id
in case no client id is provided to the api client """

CLIENT_SECRET = None
""" The secret value to be used for situations where
no client secret has been provided to the client """

REDIRECT_URL = "http://localhost:8080/oauth"
""" The redirect url used as default (fallback) value
in case none is provided to the api (client) """

SCOPE = (
    "basic",
    "public_content"
)
""" The list of permissions to be used to create the
scope string for the oauth value """

class Api(
    appier.OAuth2Api,
    tag.TagApi,
    user.UserApi,
    media.MediaApi,
    subscription.SubscriptionApi
):

    def __init__(self, *args, **kwargs):
        appier.OAuth2Api.__init__(self, *args, **kwargs)
        self.client_id = appier.conf("INSTAGRAM_ID", CLIENT_ID)
        self.client_secret = appier.conf("INSTAGRAM_SECRET", CLIENT_SECRET)
        self.redirect_url = appier.conf("INSTAGRAM_REDIRECT_URL", REDIRECT_URL)
        self.base_url = kwargs.get("base_url", BASE_URL)
        self.client_id = kwargs.get("client_id", self.client_id)
        self.client_secret = kwargs.get("client_secret", self.client_secret)
        self.redirect_url = kwargs.get("redirect_url", self.redirect_url)
        self.scope = kwargs.get("scope", SCOPE)
        self.access_token = kwargs.get("access_token", None)
        self.user_id = kwargs.get("user_id", None)

    def oauth_authorize(self, state = None):
        url = self.base_url + "oauth/authorize"
        values = dict(
            client_id = self.client_id,
            redirect_uri = self.redirect_url,
            response_type = "code",
            scope = " ".join(self.scope)
        )
        if state: values["state"] = state.encode("utf-8")
        data = appier.legacy.urlencode(values)
        url = url + "?" + data
        return url

    def oauth_access(self, code):
        url = self.base_url + "oauth/access_token"
        contents = self.post(
            url,
            token = False,
            client_id = self.client_id,
            client_secret = self.client_secret,
            grant_type = "authorization_code",
            redirect_uri = self.redirect_url,
            code = code
        )
        self.access_token = contents["access_token"]
        self.user_id = contents["user"]["id"]
        self.trigger("access_token", self.access_token)
        self.trigger("user_id", self.user_id)
        return self.access_token
