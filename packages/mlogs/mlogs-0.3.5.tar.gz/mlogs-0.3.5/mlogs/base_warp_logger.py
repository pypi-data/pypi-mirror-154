#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/9 3:24 PM
# @Author  : chenDing

from .base_logger import BaseLogger


class BaseWarpLogger(BaseLogger):
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)

    def debug(self, msg, trace_id='', topic=''):
        self._logger.bind(call_info=self._format_handler.call_info()).debug(
            self._format_handler.format_args(self, msg, trace_id, topic))

    def info(self, msg, trace_id='', topic=''):
        self._logger.bind(call_info=self._format_handler.call_info()).info(
            self._format_handler.format_args(self, msg, trace_id, topic))

    def warning(self, msg, trace_id='', topic=''):
        self._logger.bind(call_info=self._format_handler.call_info()).warning(
            self._format_handler.format_args(self, msg, trace_id, topic))

    def error(self, msg, trace_id='', topic=''):
        self._logger.bind(call_info=self._format_handler.call_info()).error(
            self._format_handler.format_args(self, msg, trace_id, topic))

    def critical(self, msg, trace_id='', topic=''):
        self._logger.bind(call_info=self._format_handler.call_info()).critical(
            self._format_handler.format_args(self, msg, trace_id, topic))

    def exception(self, msg: str, trace_id='', topic=''):
        """异常，默认把 msg 转为 str格式 """
        self._logger.opt(exception=True).bind(call_info=self._format_handler.call_info()).exception(
            self._format_handler.format_args(self, str(msg), trace_id, topic))
