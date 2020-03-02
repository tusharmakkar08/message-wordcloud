__author__ = 'Tushar Makkar <tmakkar@eightfold.ai>'

import logging

from enum import Enum


class MessageCategory(Enum):
    FACEBOOK = 1
    WHATSAPP = 2
    INSTAGRAM = 3
    HIKE = 4


class Message:
    def __init__(self, content, sender):
        self._content = content
        self._sender = sender

    def get_content(self):
        return self._content

    def get_sender(self):
        return self._sender


class MessageMedium:
    def __init__(self, file_name):
        self._file_name = file_name

    def _read_file(self):
        with open(self._file_name) as f:
            return f.read()

    def convert_to_messages(self):
        return


class FacebookMessageMedium(MessageMedium):
    def convert_to_messages(self):
        pass


class WhatsappMessageMedium(MessageMedium):
    def convert_to_messages(self):
        pass


class InstagramMessageMedium(MessageMedium):
    def convert_to_messages(self):
        pass


class HikeMessageMedium(MessageMedium):
    def convert_to_messages(self):
        pass


class MessageWordCloud:
    def __init__(self, logger, data_map):
        self._logger = logger
        self._data_map = data_map
        self._class_map = {
        }

    def build_final_data_js_file(self):
        return


if __name__ == '__main__':
    _logger = logging.getLogger()
    _data_map = {
        MessageCategory.FACEBOOK: 'data/fb.json',
        MessageCategory.HIKE: 'data/hike.txt',
        MessageCategory.INSTAGRAM: 'data/ig.json',
        MessageCategory.WHATSAPP: 'data/wp.txt'
    }
    MessageWordCloud(_logger, _data_map).build_final_data_js_file()
