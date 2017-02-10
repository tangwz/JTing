# coding: utf-8
"""
    jting.ettings
    ~~~~~~~~~~~~~~~~~~~~

    This is the jting's settings.

    description:
        Settings of specific database and config parameters.
"""

import datetime

SITE_NAME = 'JTING'
SITE_DESCRIPTION = 'JTing is a API-based platform.'
SITE_YEAR = datetime.date.today().year


class AttributeClass(dict):
    def __getattr__(self, item):
        return dict.__getitem__(self, item)


ALL_PERMS = {
    "SUPER_ADMIN": AttributeClass({"id": "9", "name": u"超级管理"}),
    "ROLE_ADMIN" : AttributeClass({"id": "1", "name": u"角色管理"}),
    "GUEST"      : AttributeClass({"id": "0", "name": u"普通用户"})
}
