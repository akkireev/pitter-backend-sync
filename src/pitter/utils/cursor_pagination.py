from base64 import b64decode, b64encode
from collections import namedtuple, OrderedDict
from urllib import parse

from rest_framework.pagination import _positive_int
from rest_framework.settings import api_settings
from rest_framework.utils.urls import replace_query_param

Cursor = namedtuple('Cursor', ['offset', 'position'])


class CursorPagination:
    cursor_query_param = 'cursor'
    page_size = api_settings.PAGE_SIZE
    offset_cutoff = 1000

    def paginate_queryset(self, queryset, request, ordering_fields: list):
        self.base_url = request.build_absolute_uri()
        self.ordering = ordering_fields

        self.cursor = self.decode_cursor(request)
        if self.cursor is None:
            (offset, current_position) = (0, None)
        else:
            (offset, current_position) = self.cursor

        queryset = queryset.order_by(*self.ordering)

        if current_position is not None:
            order = self.ordering[0]
            is_reversed = order.startswith('-')
            order_attr = order.lstrip('-')

            if is_reversed:
                kwargs = {order_attr + '__lt': current_position}
            else:
                kwargs = {order_attr + '__gt': current_position}

            queryset = queryset.filter(**kwargs)

        results = list(queryset[offset:offset + self.page_size + 1])
        self.page = list(results[:self.page_size])
        if len(results) > len(self.page):
            has_following_position = True
            following_position = self._get_position_from_instance(results[-1], self.ordering)
        else:
            has_following_position = False
            following_position = None

        self.has_next = has_following_position
        self.has_previous = (current_position is not None) or (offset > 0)
        if self.has_next:
            self.next_position = following_position
        if self.has_previous:
            self.previous_position = current_position

        return self.page

    def get_next_link(self):
        if not self.has_next:
            return None

        compare = self.next_position
        offset = 0

        has_item_with_unique_position = False
        for item in reversed(self.page):
            position = self._get_position_from_instance(item, self.ordering)
            if position != compare:
                has_item_with_unique_position = True
                break

            compare = position
            offset += 1

        if self.page and not has_item_with_unique_position:
            if not self.has_previous:
                offset = self.page_size
                position = None
            else:
                offset = self.cursor.offset + self.page_size
                position = self.previous_position

        if not self.page:
            position = self.next_position

        cursor = Cursor(offset=offset, position=position)
        return self.encode_cursor(cursor)

    def decode_cursor(self, request):
        encoded = request.query_params.get(self.cursor_query_param)
        if encoded is None:
            return None

        try:
            querystring = b64decode(encoded.encode('ascii')).decode('ascii')
            tokens = parse.parse_qs(querystring, keep_blank_values=True)

            offset = tokens.get('o', ['0'])[0]
            offset = _positive_int(offset, cutoff=self.offset_cutoff)

            position = tokens.get('p', [None])[0]
        except (TypeError, ValueError):
            raise ValueError('Invalid cursor')

        return Cursor(offset=offset, position=position)

    def encode_cursor(self, cursor):
        tokens = {}
        if cursor.offset != 0:
            tokens['o'] = str(cursor.offset)
        if cursor.position is not None:
            tokens['p'] = cursor.position

        querystring = parse.urlencode(tokens, doseq=True)
        encoded = b64encode(querystring.encode('ascii')).decode('ascii')
        return replace_query_param(self.base_url, self.cursor_query_param, encoded)

    def _get_position_from_instance(self, instance, ordering):
        field_name = ordering[0].lstrip('-')
        if isinstance(instance, dict):
            attr = instance[field_name]
        else:
            attr = getattr(instance, field_name)
        return str(attr)

    def get_paginated_dict(self, data):
        return OrderedDict([
            ('next', self.get_next_link()),
            ('results', data)
        ])
