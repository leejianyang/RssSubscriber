# -*- coding:utf-8 -*-
"""
app.action.entry_action
~~~~~~~~~~~~~~~~~~~~~~~~

与entry有关的业务逻辑
"""
from rss.models.entry_model import EntryModel


class EntryAction(object):

    @classmethod
    def update(cls, entry_id, unread=None, marked=None):
        """
        修改entry的属性
        """
        if unread is not None:
            EntryModel.read(entry_id)
