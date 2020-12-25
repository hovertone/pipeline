#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2018
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
import pytest

from telegram import Update, Message, Chat, User, TelegramError
from telegram.ext import CallbackContext


class TestCallbackContext(object):
    def test_non_context_dp(self, dp):
        with pytest.raises(ValueError):
            CallbackContext(dp)

    def test_from_job(self, cdp):
        job = cdp.job_queue.run_once(lambda x: x, 10)

        callback_context = CallbackContext.from_job(job, cdp)

        assert callback_context.job is job
        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

    def test_from_update(self, cdp):
        update = Update(0, message=Message(0, User(1, 'user', False), None, Chat(1, 'chat')))

        callback_context = CallbackContext.from_update(update, cdp)

        assert callback_context.chat_data == {}
        assert callback_context.user_data == {}
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

        callback_context_same_user_chat = CallbackContext.from_update(update, cdp)

        callback_context.chat_data['test'] = 'chat'
        callback_context.user_data['test'] = 'user'

        assert callback_context_same_user_chat.chat_data is callback_context.chat_data
        assert callback_context_same_user_chat.user_data is callback_context.user_data

        update_other_user_chat = Update(0, message=Message(0, User(2, 'user', False),
                                                           None, Chat(2, 'chat')))

        callback_context_other_user_chat = CallbackContext.from_update(update_other_user_chat, cdp)

        assert callback_context_other_user_chat.chat_data is not callback_context.chat_data
        assert callback_context_other_user_chat.user_data is not callback_context.user_data

    def test_from_update_not_update(self, cdp):
        callback_context = CallbackContext.from_update(None, cdp)

        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

        callback_context = CallbackContext.from_update('', cdp)

        assert callback_context.chat_data is None
        assert callback_context.user_data is None
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

    def test_from_error(self, cdp):
        error = TelegramError('test')

        update = Update(0, message=Message(0, User(1, 'user', False), None, Chat(1, 'chat')))

        callback_context = CallbackContext.from_error(update, error, cdp)

        assert callback_context.error is error
        assert callback_context.chat_data == {}
        assert callback_context.user_data == {}
        assert callback_context.bot is cdp.bot
        assert callback_context.job_queue is cdp.job_queue
        assert callback_context.update_queue is cdp.update_queue

    def test_match(self, cdp):
        callback_context = CallbackContext(cdp)

        assert callback_context.match is None

        callback_context.matches = ['test', 'blah']

        assert callback_context.match == 'test'
