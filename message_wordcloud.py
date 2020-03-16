__author__ = 'Tushar Makkar <tmakkar@eightfold.ai>'

import argparse
import collections
import json
import logging
import os
import os.path
import sys

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

    def convert_to_messages(self, participants=None):
        return


class FacebookMessageMedium(MessageMedium):
    def convert_to_messages(self, participants=None):
        data = self._read_file()
        actual_data = data['messages']
        list_of_messages = []
        for i in actual_data:
            if i.get('content'):
                list_of_messages.append(Message(i['content'], i['sender_name']))
        return list_of_messages


class WhatsappMessageMedium(MessageMedium):
    def convert_to_messages(self, participants=None):
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
            if set(participants) == set(i['participants']):
                actual_data = i
                break
        list_of_messages = []
        for i in actual_data['conversation']:
            if i.get('text'):
                list_of_messages.append(Message(i.get('text'), i.get('sender')))
        return list_of_messages


class HikeMessageMedium(MessageMedium):
    def convert_to_messages(self, participants=None):
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
        self._stopwords = []
        self._get_stopwords()

    def _get_stopwords(self):
        data_files = ['assets/' + i for i in os.listdir('assets')]
        for i in data_files:
            with open(i) as f:
                self._stopwords.extend(f.readlines())
        self._stopwords = set([i.strip().lower() for i in self._stopwords])

    def convert_to_frequency(self, all_messages, msg_category, chop_off_num):
        data_dict = collections.defaultdict(lambda: collections.defaultdict(int))
        min_length = 10 ** 10
        for data_msg_category in all_messages:
            if msg_category == data_msg_category or msg_category == 'all':
                for msg in all_messages[data_msg_category]:
                    actual_message = msg.get_content()
                    split_message = actual_message.split()
                    for word in split_message:
                        if len(word) > 2 and word.lower() not in self._stopwords and word.isalnum():
                            data_dict[data_msg_category.name][word.lower()] += 1
                data_dict[data_msg_category.name] = sorted(data_dict[data_msg_category.name].items(), key=lambda x: -1 * x[1])
                data_dict[data_msg_category.name] = [i for i in data_dict[data_msg_category.name] if i[1] > chop_off_num]
                min_length = min(len(data_dict[data_msg_category.name]), min_length)
        for data_msg_category in data_dict:
            data_dict[data_msg_category] = data_dict[data_msg_category][:min_length]
        return data_dict

    @staticmethod
    def _make_js(freq_map):
        data_list = []
        for data in freq_map:
            for ind_word_cnt in freq_map[data]:
                data_list.append({"x": str(ind_word_cnt[0]), "value": ind_word_cnt[1], "category": data})
        main_string = "let data = %s" % data_list
        main_string = main_string.replace("'", '"')
        with open('final_data.js', 'w') as f:
            f.write(main_string)

    def build_final_data_js_file(self, participants_ig_name, freq_chop_off_num=2):
        all_messages = {}
        for type_of_message in self._class_map:
            self._logger.info("Getting messages for %s" % type_of_message)
            all_messages[type_of_message] = self._class_map[type_of_message](self._data_map[type_of_message]).convert_to_messages(
                participants=participants_ig_name)
        freq_map = self.convert_to_frequency(all_messages, 'all', freq_chop_off_num)
        self._make_js(freq_map)


if __name__ == '__main__':
    _logger = logging.getLogger()
    _logger.setLevel(logging.DEBUG)
    _ch = logging.StreamHandler(sys.stdout)
    _ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    _logger.addHandler(_ch)
    args = argparse.ArgumentParser(description='Argument parser for wordcloud')
    args.add_argument('--ig_names', help='Instagram name list', type=str, required=True, nargs=2)
    args.add_argument('--folder', help='Folder where files are present', type=str, required=True)
    args = args.parse_args()
    _data_map = {
        MessageCategory.FACEBOOK: os.path.join(args.folder, 'fb.json'),
        MessageCategory.HIKE: os.path.join(args.folder, 'hike.txt'),
        MessageCategory.INSTAGRAM: os.path.join(args.folder, 'ig.json'),
        MessageCategory.WHATSAPP: os.path.join(args.folder, 'wp.txt')
    }
    MessageWordCloud(_logger, _data_map).build_final_data_js_file(args.ig_names, 0)
