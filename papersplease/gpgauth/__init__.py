# -*- coding: utf-8 -*-

from gnupg import GPG
import random


def create_gpg_object(**gpg_options):
    gpg = gpg_options.pop('gpg', None)
    if not gpg:
        gpg = GPG(**gpg_options)
        gpg.encoding = 'utf-8'
    return gpg


def hex_key_id(int_id):
    return b'0x{}'.format(hex(int_id).upper()[2:-1])


def import_key_from_server(keyserver, user_key_id, **gpg_options):
    gpg = create_gpg_object(**gpg_options)
    gpg.recv_keys(keyserver, hex_key_id(user_key_id))


def generate(user_key_id, word_list, word_count, **gpg_options):
    gpg = create_gpg_object(**gpg_options)
    words = ' '.join(random.sample(word_list, word_count))
    return words, gpg.encrypt(words, hex_key_id(user_key_id),
                              always_trust=True)
