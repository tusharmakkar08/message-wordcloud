__author__ = 'Tushar Makkar <tmakkar@eightfold.ai>'

import json
import logging
import os.path

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
        extension = os.path.splitext(self._file_name)[1][1:].strip()
        if extension == 'txt':
            with open(self._file_name) as f:
                return f.read()
        elif extension == 'json':
            with open(self._file_name) as f:
                return json.load(f)
        return None

    def convert_to_messages(self):
        return


class FacebookMessageMedium(MessageMedium):
    def convert_to_messages(self):
        data = self._read_file()
        actual_data = data['messages']
        list_of_messages = []
        for i in actual_data:
            if i.get('content'):
                list_of_messages.append(Message(i['content'], i['sender_name']))
        return list_of_messages


class WhatsappMessageMedium(MessageMedium):
    def convert_to_messages(self):
        data = self._read_file()
        chat_data = data.split('\n')[1:]
        participants = set()
        for data in chat_data:
            if len(participants) >= 2:
                break
            participants.add(data.split(' - ')[-1].split(':')[0])
        participants = list(participants)
        participants = [i + ': ' for i in participants]
        list_of_messages = []
        for data in chat_data:
            sender = None
            for i in participants:
                if i in data:
                    sender = i
                    break
            if data and sender:
                list_of_messages.append(Message(data.split(sender)[-1], sender[:-2]))
        return list_of_messages


class InstagramMessageMedium(MessageMedium):
    def convert_to_messages(self, participants=None):
        data = self._read_file()
        actual_data = None
        for i in data:
            if participants == i['participants']:
                actual_data = i
                break
        list_of_messages = []
        for i in actual_data['conversation']:
            if i.get('text'):
                list_of_messages.append(Message(i.get('text'), i.get('sender')))
        return list_of_messages


class HikeMessageMedium(MessageMedium):
    def convert_to_messages(self):
        data = self._read_file()
        line_data = data.split('\n')
        chat_data = line_data[1:]
        participants = ['me-', line_data[0].split('Chat with ')[-1] + '-']
        list_of_messages = []
        for data in chat_data:
            sender = None
            for i in participants:
                if i in data:
                    sender = i
                    break
            if data and sender:
                list_of_messages.append(Message(data.split(sender)[-1], sender[:-1]))
        return list_of_messages


class MessageWordCloud:
    def __init__(self, logger, data_map):
        self._logger = logger
        self._data_map = data_map
        self._class_map = {
            MessageCategory.WHATSAPP: WhatsappMessageMedium,
            MessageCategory.HIKE: HikeMessageMedium,
            MessageCategory.FACEBOOK: FacebookMessageMedium,
            MessageCategory.INSTAGRAM: InstagramMessageMedium
        }

    def build_final_data_js_file(self):
        data = HikeMessageMedium(self._data_map[MessageCategory.HIKE]).convert_to_messages()
        data = WhatsappMessageMedium(self._data_map[MessageCategory.WHATSAPP]).convert_to_messages()
        data = InstagramMessageMedium(self._data_map[MessageCategory.INSTAGRAM]).convert_to_messages(participants=["a", "b"])
        data = FacebookMessageMedium(self._data_map[MessageCategory.FACEBOOK]).convert_to_messages()


if __name__ == '__main__':
    _logger = logging.getLogger()
    _data_map = {
        MessageCategory.FACEBOOK: 'data/fb.json',
        MessageCategory.HIKE: 'data/hike.txt',
        MessageCategory.INSTAGRAM: 'data/ig.json',
        MessageCategory.WHATSAPP: 'data/wp.txt'
    }
    MessageWordCloud(_logger, _data_map).build_final_data_js_file()
