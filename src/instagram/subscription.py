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

class SubscriptionApi(object):

    def subscribe(self, object = "tag", aspect = "media", object_id = None, callback_url = None):
        url = self.base_url + "v1/subscriptions"
        contents = self.get(
            url,
            token = False,
            client_id = self.client_id,
            client_secret = self.client_secret,
            object = object,
            aspect = aspect,
            object_id = object_id,
            callback_url = callback_url
        )
        return contents["data"]

    def unsubscribe(self, object = "tag", aspect = "media", object_id = None, callback_url = None):
        url = self.base_url + "v1/subscriptions"
        contents = self.delete(
            url,
            token = False,
            client_id = self.client_id,
            client_secret = self.client_secret,
            object = object,
            aspect = aspect,
            object_id = object_id,
            callback_url = callback_url
        )
        return contents["data"]
