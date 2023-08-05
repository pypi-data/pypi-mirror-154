#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/9 3:27 PM
# @Author  : chenDing
from typing import Optional
from .stdout_logger import StdoutLogger
from .utils import NumpyEncoder


class AdaptHistoryLogger(StdoutLogger):
    """兼容历史日志"""

    def __init__(self, config: Optional[dict] = None, level: Optional[str] = None, json_encoder=None,
                 *args, **kwargs):
        """
        :param config:  loguru 配置
        :param level:  指定日志 级别
        """
        # ⚠️ json_encoder 位置在 第三个，对应的 base logger 位置
        # 为什么 json_encoder: Optional[Type[JSONEncoder]] 的值会跑过来，去 赋值给到 json_encoder？ 因为
        # kwargs 解包不是那么智能。 json_encoder 需要手动放到 kwargs 中。 否则，会被送到 args 里面。导致第三个 json_encoder 被赋值
        # 规定： 继承参数传值时。最好 被继承和 继承，一一对应，如果不能对应，则应该手动 放入到 kwargs 中
        kwargs["json_encoder"] = json_encoder or NumpyEncoder
        super().__init__(config, level, *args, **kwargs)

    def debug(self, trace_id, topic, msg):
        self._logger.bind(call_info=self._call_info()).debug(self._format_args(msg, trace_id, topic))

    def info(self, trace_id, topic, msg):
        self._logger.bind(call_info=self._call_info()).info(self._format_args(msg, trace_id, topic))

    def warning(self, trace_id, topic, msg):
        self._logger.bind(call_info=self._call_info()).warning(
            self._format_args(msg, trace_id, topic))

    def error(self, trace_id, topic, msg):
        self._logger.bind(call_info=self._call_info()).error(self._format_args(msg, trace_id, topic))

    def critical(self, trace_id, topic, msg):
        self._logger.bind(call_info=self._call_info()).critical(
            self._format_args(msg, trace_id, topic))

    def exception(self, trace_id, topic, msg: str):
        """异常，默认把 msg 转为 str格式 """
        self._logger.opt(exception=True).bind(call_info=self._call_info()).exception(
            self._format_args(str(msg), trace_id, topic))
