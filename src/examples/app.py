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

from . import base

class InstagramApp(appier.WebApp):

    def __init__(self, *args, **kwargs):
        appier.WebApp.__init__(
            self,
            name = "instagram",
            *args, **kwargs
        )

    @appier.route("/", "GET")
    def index(self):
        return self.me()

    @appier.route("/me", "GET")
    def me(self):
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        user = api.self_user()
        return user

    @appier.route("/oauth", "GET")
    def oauth(self):
        code = self.field("code")
        api = self.get_api()
        access_token = api.oauth_access(code)
        self.session["ig.access_token"] = access_token
        self.session["ig.user_id"] = api.user_id
        return self.redirect(
            self.url_for("instagram.index")
        )

    @appier.exception_handler(appier.OAuthAccessError)
    def oauth_error(self, error):
        if "ig.access_token" in self.session: del self.session["ig.access_token"]
        if "ig.user_id" in self.session: del self.session["ig.user_id"]
        return self.redirect(
            self.url_for("instagram.index")
        )

    def ensure_api(self):
        access_token = self.session.get("ig.access_token", None)
        if access_token: return
        api = base.get_api()
        return api.oauth_authorize()

    def get_api(self):
        access_token = self.session and self.session.get("ig.access_token", None)
        user_id = self.session and self.session.get("ig.user_id", None)
        api = base.get_api()
        api.access_token = access_token
        api.user_id = user_id
        return api

if __name__ == "__main__":
    app = InstagramApp()
    app.serve()
else:
    __path__ = []
