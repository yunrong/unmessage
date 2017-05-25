import json

import attr
from nacl.utils import random
from pyaxo import b2a


class Element(dict):
    def __init__(self, sender, receiver, type_, id_, part_len):
        self.sender = sender
        self.receiver = receiver
        self.type_ = type_
        self.id_ = id_
        self.part_len = part_len

    def __str__(self):
        return ''.join(self.values())

    @property
    def is_complete(self):
        return len(self) == self.part_len


@attr.s
class ElementPayload(object):
    filtered_attr_names = None

    content = attr.ib(default=None)

    @classmethod
    def filter_attrs(cls, attribute, value):
        if cls.filtered_attr_names is None:
            return True
        else:
            return attribute.name in cls.filtered_attr_names

    @classmethod
    def deserialize(cls, data):
        return cls(**json.loads(data))

    def serialize(self):
        return json.dumps(attr.asdict(self, filter=self.filter_attrs))


class RequestElement:
    type_ = 'req'
    request_accepted = 'accepted'


class UntalkElement:
    type_ = 'untalk'


class PresenceElement:
    type_ = 'pres'
    status_online = 'online'
    status_offline = 'offline'


class MessageElement:
    type_ = 'msg'


class AuthenticationElement:
    type_ = 'auth'


REGULAR_ELEMENT_TYPES = [RequestElement.type_,
                         PresenceElement.type_,
                         MessageElement.type_,
                         AuthenticationElement.type_]


ID_LENGTH = 2


def get_random_id():
    return b2a(random(ID_LENGTH))
