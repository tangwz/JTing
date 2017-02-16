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
    "USER_MANAGE": AttributeClass({"id": "1", "name": u"用户管理"}),
    "ROLE_MANAGE": AttributeClass({"id": "2", "name": u"角色管理"}),

    "TOPIC_MANAGE": AttributeClass({"id": "3", "name": u"话题管理"}),
    "COCO_MANAGE": AttributeClass({"id": "4", "name": u"分类管理"})
}
