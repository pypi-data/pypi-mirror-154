import os
import string
import random
import logging
from typing import List, Union

import requests

logger = logging.getLogger(__name__)

ACCESS_TOKEN = None
ACCESS_TOKEN_ENV_NAME = 'SLACK_ACCESS_TOKEN'

COLOR_MAP = {
    'green': '#008000',
    'gray': '#808080',
    'red': '#FF0000',
    'blue': '#0000FF',
    'black': '#000000',
    'yellow': '#FFFF00',
    'maroon': '#800000',
    'purple': '#800080',
    'olive': '#808000',
    'silver': '#C0C0C0',
    'gold': '#FFD700',
    'pink': '#FFC0CB',
    'coral': '#FF7F50',
    'brown': '#A52A2A',
    'indigo': '#4B0082',
    'aqua': '#00FFFF',
    'cyan': '#00FFFF',
    'lime': '#00FF00',
    'teal': '#008080',
    'navy': '#000080',
    'sienna': '#A0522D',
}


def _random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class SlackError(requests.exceptions.RequestException):
    pass


class Resource:

    def __init__(self, handle: str, method: str):
        self.handle = handle
        self.method = method


class DictConvertibleObject:

    def __init__(self, *args, **kwargs):
        pass

    def to_dict(self):
        raise NotImplementedError(
            'Object "{}" does not implemented "to_dict" method'.format(self.__class__.__name__),
        )


class AttachmentField(DictConvertibleObject):

    def __init__(self, *, title: str = None, value: str = None, short: bool = False):
        super(AttachmentField, self).__init__()

        self.title = title
        self.value = value
        self.short = short

    def to_dict(self):
        assert self.title is not None or self.value is not None, \
            'Title or value is required for attachment field'

        data = {'short': self.short}

        if self.title:
            data['title'] = self.title

        if self.value:
            data['value'] = self.value

        return data


class Attachment(DictConvertibleObject):
    Field = AttachmentField

    def __init__(self, *,
                 image_url: str = None,
                 thumb_url: str = None,
                 author_name: str = None,
                 author_link: str = None,
                 author_icon: str = None,
                 title: str = None,
                 title_link: str = None,
                 text: str = None,
                 pretext: str = None,
                 footer: str = None,
                 footer_icon: str = None,
                 timestamp: str = None,
                 fields: List[AttachmentField] = None,
                 mrkdwn: bool = True,
                 color: str = None):
        super(Attachment, self).__init__()

        self.image_url = image_url
        self.thumb_url = thumb_url

        self.author_name = author_name
        self.author_link = author_link
        self.author_icon = author_icon

        self.title = title
        self.title_link = title_link

        self.text = text

        self.pretext = pretext

        self.footer = footer
        self.footer_icon = footer_icon

        self.timestamp = timestamp

        self.fields = fields

        self.mrkdwn = mrkdwn
        self.color = color

    def to_dict(self):
        data = {
            'mrkdwn_in': [],
        }

        if self.color:
            data['color'] = COLOR_MAP.get(self.color, self.color)

        if self.image_url:
            data['image_url'] = self.image_url

        if self.thumb_url:
            data['thumb_url'] = self.thumb_url

        if self.author_name:
            data['author_name'] = self.author_name

        if self.author_link:
            data['author_link'] = self.author_link

        if self.author_icon:
            data['author_icon'] = self.author_icon

        if self.title:
            data['title'] = self.title
            if self.mrkdwn:
                data['mrkdwn_in'].append('title')

        if self.title_link:
            data['title_link'] = self.title_link

        if self.pretext:
            data['pretext'] = self.pretext
            if self.mrkdwn:
                data['mrkdwn_in'].append('pretext')

        if self.text:
            data['text'] = self.text
            if self.mrkdwn:
                data['mrkdwn_in'].append('text')

        if self.footer:
            data['footer'] = self.footer
            if self.mrkdwn:
                data['mrkdwn_in'].append('footer')

        if self.footer_icon:
            data['footer_icon'] = self.footer_icon

        if self.timestamp:
            data['ts'] = self.timestamp

        if self.fields:
            data['fields'] = [f.to_dict() for f in self.fields]
            if self.mrkdwn:
                data['mrkdwn_in'].append('fields')

        return data


class BaseBlock(DictConvertibleObject):
    __type__ = None

    def __init__(self, *, mrkdwn: bool = True, block_id: str = None):
        super(BaseBlock, self).__init__()

        self.mrkdwn = mrkdwn
        self.block_id = block_id
        self.content_type = 'mrkdwn' if self.mrkdwn else 'plain_text'

    def to_dict(self):
        data = {
            'type': self.__type__,
        }

        if self.block_id:
            data['block_id'] = self.block_id

        return data


class BaseBlockField(DictConvertibleObject):
    __type__ = None

    def __init__(self, *, mrkdwn=True):
        super(BaseBlockField, self).__init__()

        self.mrkdwn = mrkdwn
        self.content_type = 'mrkdwn' if self.mrkdwn else 'plain_text'

    def to_dict(self):
        if self.__type__:
            return {
                'type': self.__type__,
            }

        return {}


class HeaderBlock(BaseBlock):
    __type__ = 'header'

    def __init__(self, text: str, **kwargs):
        kwargs['mrkdwn'] = False
        super().__init__(**kwargs)

        self.text = text

    def to_dict(self):
        data = super().to_dict()

        data['text'] = {
            'type': self.content_type,
            'text': self.text,
        }

        return data


class SimpleTextBlockField(BaseBlockField):

    def __init__(self, text: str, *, emoji: bool = None, **kwargs):
        super(SimpleTextBlockField, self).__init__(**kwargs)

        self.text = text
        self.emoji = emoji

    def to_dict(self):
        data = super(SimpleTextBlockField, self).to_dict()

        data['text'] = self.text
        data['type'] = self.content_type

        if self.emoji is not None:
            data['emoji'] = self.emoji

        return data


class SimpleTextBlock(BaseBlock):
    __type__ = 'section'

    Field = SimpleTextBlockField

    def __init__(self, text: str, *, fields: List[SimpleTextBlockField] = None, **kwargs):
        super(SimpleTextBlock, self).__init__(**kwargs)

        self.text = text
        self.fields = fields

    def to_dict(self):
        data = super(SimpleTextBlock, self).to_dict()

        data['text'] = {
            'type': self.content_type,
            'text': self.text,
        }

        if self.fields:
            data['fields'] = [f.to_dict() for f in self.fields]

        return data


class DividerBlock(BaseBlock):
    __type__ = 'divider'


class ImageBlock(BaseBlock):
    __type__ = 'image'

    def __init__(self, image_url, *, title: str = None, alt_text: str = None, **kwargs):
        super(ImageBlock, self).__init__(**kwargs)

        self.image_url = image_url

        self.title = title
        self.alt_text = alt_text or image_url

    def to_dict(self):
        data = super(ImageBlock, self).to_dict()

        data['image_url'] = self.image_url

        if self.title:
            data['title'] = {
                'type': self.content_type,
                'text': self.title,
            }

        if self.alt_text:
            data['alt_text'] = self.alt_text

        return data


class ContextBlockTextElement(BaseBlockField):

    def __init__(self, text, **kwargs):
        super(ContextBlockTextElement, self).__init__(**kwargs)

        self.text = text

    def to_dict(self):
        data = super(ContextBlockTextElement, self).to_dict()

        data['text'] = self.text
        data['type'] = self.content_type

        return data


class ContextBlockImageElement(BaseBlockField):
    __type__ = 'image'

    def __init__(self, image_url, alt_text: str = None):
        super(ContextBlockImageElement, self).__init__()

        self.image_url = image_url
        self.alt_text = alt_text

    def to_dict(self):
        data = super(ContextBlockImageElement, self).to_dict()

        data['image_url'] = self.image_url

        if self.alt_text:
            data['alt_text'] = self.alt_text

        return data


class ContextBlock(BaseBlock):
    __type__ = 'context'

    TextElement = ContextBlockTextElement
    ImageElement = ContextBlockImageElement

    def __init__(self, elements: List[Union[ContextBlockTextElement, ContextBlockImageElement]], **kwargs):
        super(ContextBlock, self).__init__(**kwargs)

        self.elements = elements

    def to_dict(self):
        data = super(ContextBlock, self).to_dict()

        data['elements'] = [e.to_dict() for e in self.elements]

        return data


def init_color(name, code):
    COLOR_MAP[name] = code


class Message:

    def __init__(self, client, response,
                 text: str = None,
                 raise_exc=False,
                 attachments: List[Attachment] = None,
                 blocks: List[BaseBlock] = None):
        self._client = client
        self._response = response
        self._raise_exc = raise_exc

        self.text = text
        self.attachments = attachments or []
        self.blocks = blocks or []

        self.__lock_thread = False

    @property
    def response(self):
        return self._response

    def _lock_thread(self):
        self.__lock_thread = True

    def add_reaction(self, name, raise_exc=False):
        json = self._response.json()
        data = {
            'name': name,
            'channel': json['channel'],
            'timestamp': json['message']['ts'],
        }
        return self._client.call_resource(
            Resource('reactions.add', 'POST'),
            json=data, raise_exc=raise_exc,
        )

    def remove_reaction(self, name, raise_exc=False):
        json = self._response.json()
        data = {
            'name': name,
            'channel': json['channel'],
            'timestamp': json['message']['ts'],
        }
        return self._client.call_resource(
            Resource('reactions.remove', 'POST'),
            json=data, raise_exc=raise_exc,
        )

    def send_to_thread(self, **kwargs):
        if self.__lock_thread:
            raise SlackError('Cannot open thread for thread message')

        json = self._response.json()
        thread_ts = json['message']['ts']
        kwargs.update(thread_ts=thread_ts)

        message = self._client.send_notify(json['channel'], **kwargs)

        lock_thread = getattr(message, '_lock_thread')
        lock_thread()

        return message

    def update(self):
        json = self._response.json()
        data = {
            'channel': json['channel'],
            'ts': json['message']['ts'],
        }

        if self.text:
            data['text'] = self.text

        if self.blocks:
            data['blocks'] = [b.to_dict() for b in self.blocks]

        if self.attachments:
            data['attachments'] = [a.to_dict() for a in self.attachments]

        return self._client.call_resource(
            Resource('chat.update', 'POST'),
            json=data, raise_exc=self._raise_exc,
        )

    def delete(self):
        json = self._response.json()
        data = {
            'channel': json['channel'],
            'ts': json['message']['ts'],
        }
        return self._client.call_resource(
            Resource('chat.update', 'POST'),
            json=data, raise_exc=self._raise_exc,
        )

    def upload_file(self, file, **kwargs):
        json = self._response.json()
        kwargs.update(thread_ts=json['message']['ts'])
        return self._client.upload_file(json['channel'], file, **kwargs)


class Slack(requests.Session):
    API_URL = 'https://slack.com/api'

    DEFAULT_RECORDS_LIMIT = 100
    DEFAULT_REQUEST_TIMEOUT = 180

    def __init__(self, token):
        super(Slack, self).__init__()

        self.headers['Authorization'] = 'Bearer {}'.format(token)
        self.headers['Content-Type'] = 'application/json; charset=utf-8'

    @classmethod
    def from_env(cls):
        token = ACCESS_TOKEN or os.getenv(ACCESS_TOKEN_ENV_NAME)
        assert token is not None, 'Please export "{}" environment variable'.format(ACCESS_TOKEN_ENV_NAME)
        return cls(token)

    def call_resource(self, resource: Resource, *, raise_exc: bool = False, **kwargs):
        kwargs.setdefault('timeout', self.DEFAULT_REQUEST_TIMEOUT)

        url = '{}/{}'.format(self.API_URL, resource.handle)
        response = self.request(resource.method, url, **kwargs)

        logger.debug(response.content)

        if raise_exc:
            response.raise_for_status()

            json = response.json()

            if not json['ok']:
                logger.error(response.content)
                raise SlackError(response.content)

        return response

    def resource_iterator(self,
                          resource: Resource, from_key: str, *,
                          cursor: str = None,
                          raise_exc: bool = False,
                          limit: int = None):
        params = {'limit': limit}

        if cursor:
            params['cursor'] = cursor

        response = self.call_resource(resource, params=params, raise_exc=raise_exc)
        data = response.json()

        for item in data[from_key]:
            yield item

        cursor = data.get('response_metadata', {}).get('next_cursor')

        if cursor:
            yield from self.resource_iterator(
                resource, from_key,
                limit=limit or self.DEFAULT_RECORDS_LIMIT, cursor=cursor, raise_exc=raise_exc,
            )

    def upload_file(self,
                    channel, file, *,
                    title: str = None,
                    content: str = None,
                    filename: str = None,
                    thread_ts: str = None,
                    filetype: str = 'text',
                    raise_exc: bool = False):
        data = {
            'channels': channel,
            'filetype': filetype,
        }
        if isinstance(file, str) and content:
            filename = file
            data.update(content=content, filename=filename)
        elif isinstance(file, str) and not content:
            data.update(filename=os.path.basename(file))
            with open(file, 'r') as f:
                data.update(content=f.read())
        else:
            data.update(content=file.read(), filename=filename or _random_string(7))

        if title:
            data.update(title=title)
        if thread_ts:
            data.update(thread_ts=thread_ts)

        return self.call_resource(
            Resource('files.upload', 'POST'),
            data=data,
            raise_exc=raise_exc,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        )

    def send_notify(self,
                    channel, *,
                    text: str = None,
                    username: str = None,
                    icon_url: str = None,
                    icon_emoji: str = None,
                    link_names: bool = True,
                    raise_exc: bool = False,
                    attachments: List[Attachment] = None,
                    blocks: List[BaseBlock] = None,
                    thread_ts: str = None):
        data = {
            'channel': channel,
            'link_names': link_names,
        }

        if username:
            data['username'] = username

        if text:
            data['mrkdwn'] = True
            data['text'] = text

        if icon_url:
            data['icon_url'] = icon_url

        if icon_emoji:
            data['icon_emoji'] = icon_emoji

        if blocks:
            data['blocks'] = [b.to_dict() for b in blocks]

        if attachments:
            data['attachments'] = [a.to_dict() for a in attachments]

        if thread_ts:
            data['thread_ts'] = thread_ts

        response = self.call_resource(
            Resource('chat.postMessage', 'POST'), raise_exc=raise_exc, json=data,
        )
        return Message(self, response, text=text, raise_exc=raise_exc, blocks=blocks, attachments=attachments)


def call_resource(*args, **kwargs):
    return Slack.from_env().call_resource(*args, **kwargs)


def resource_iterator(*args, **kwargs):
    return Slack.from_env().resource_iterator(*args, **kwargs)


def send_notify(*args, **kwargs):
    return Slack.from_env().send_notify(*args, **kwargs)
