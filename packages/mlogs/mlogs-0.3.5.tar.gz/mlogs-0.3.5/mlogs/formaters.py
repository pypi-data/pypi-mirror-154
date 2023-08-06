#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/8 7:04 PM
# @Author  : chenDing
from inspect import getframeinfo, stack
import os
import json
from json import JSONEncoder


class Format:
    format = None

    @staticmethod
    def call_info():
        """"""

    @staticmethod
    def format_args(*args, **kwargs):
        """"""


class Format1(Format):
    """"""
    format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green>, <level>{level}</level>, <cyan>{extra[call_info]}</cyan>, <level>{message}</level>"

    @staticmethod
    def call_info():
        caller = getframeinfo(stack()[2][0])
        return f'{os.path.basename(caller.filename)}:{caller.function}:line {caller.lineno}'

    @staticmethod
    def format_args(self, msg, trace_id='', topic=''):
        if not isinstance(msg, dict):
            msg = {'log': msg}
        data = {**msg}
        if trace_id:
            data["trace_id"] = trace_id
        topic = topic or self._default_topic
        if topic:
            data["topic"] = topic
        try:
            # fixme 此处有必要使用json dumps处理？为了后续解析？msg 中的数据结构，可能会导致json解析失败。
            if self._json_encoder:
                json_str = json.dumps(data, ensure_ascii=False, cls=self._json_encoder)
            else:
                json_str = json.dumps(data, ensure_ascii=False)
            return json_str[1:-1]  # 去掉前后括号
        except TypeError or JSONEncoder:
            return str(data)[1:-1].replace("'", '"')
