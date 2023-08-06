#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/9 3:27 PM
# @Author  : chenDing

"""
1. 为了兼容历史日志格式
2. 只有在报错时，才加入行数。
3. 额外封装，用字典的形式，返回日志。
4. 日志 直接输出到 stdout 即可
5. 日志里，不能打印 set ，否则 会导致json 报错。（可以在打印前 处理，但是不想）
"""
import os
import sys
from typing import Optional, List, Union
from inspect import getframeinfo, stack
import json
from datetime import datetime

from loguru import logger
from notifiers.logging import NotificationHandler

from .utils import NumpyEncoder


class AdaptHistoryLogger:

    def __init__(self, level: Optional[str] = None,
                 alerts: Optional[Union[dict, List[dict]]] = None,
                 default_topic: Optional[str] = None, ):
        if os.environ.get('DEPLOYMENT') == 'PRODUCTION':
            self._LEVEL = 'INFO'
        else:
            self._LEVEL = 'DEBUG'
        if level:
            self._LEVEL = level

        self._default_topic = default_topic or ''
        print(f"Environ: {os.environ.get('DEPLOYMENT', 'DEVELOP')}, log level is:{self._LEVEL}")
        alerts = alerts or {}
        _format = r'{message}'
        new_config = {
            "sink": sys.stdout,
            "level": self._LEVEL,
            # 使用队列，能解决多进程情况可能导致的日志被覆盖
            "enqueue": True,
            "backtrace": True,  # 允许显示整个堆栈, 允许捕获具体错误 ⚠️ 这里可能导致敏感数据泄漏。使用时需要注意
            "diagnose": True,
            # 自定义格式
            "format": _format,
        }
        logger.remove()  # 删去import logger之后自动产生的handler，不删除的话会出现重复输出的现象
        logger.add(**new_config)
        self._logger = logger
        if alerts:
            if isinstance(alerts, dict):
                n_handler = NotificationHandler(alerts["alerts_type"], defaults=alerts.get("params"))
                logger.add(n_handler, level=alerts.get("alerts_level", "ERROR"), format=_format)
            elif isinstance(alerts, list):
                for each_alert in alerts:
                    n_handler = NotificationHandler(each_alert["alerts_type"], defaults=each_alert.get("params"))
                    logger.add(n_handler, level=each_alert.get("alerts_level", "ERROR"), format=_format)
            else:
                raise TypeError("alerts must be dict or list(dict)")

    def debug(self, topic="", trace_id="", msg=""):
        self._logger.debug(self._format_args(msg, trace_id, topic, level="DEBUG"))

    def info(self, topic="", trace_id="", msg=""):
        self._logger.info(self._format_args(msg, trace_id, topic, level="INFO"))

    def warning(self, topic="", trace_id="", msg=""):
        self._logger.warning(
            self._format_args(msg, trace_id, topic, level="WARNING"))

    def error(self, topic="", trace_id="", msg=""):
        self._logger.error(self._format_args(msg, trace_id, topic, call_info=True, level="ERROR"))

    def critical(self, topic="", trace_id="", msg=""):
        self._logger.critical(self._format_args(msg, trace_id, topic, call_info=True, level="CRITICAL"))

    def exception(self, topic="", trace_id='', msg=''):
        """异常，默认把 msg 转为 str格式 """
        self._logger.opt(exception=True).exception(
            self._format_args(msg, trace_id, topic, call_info=True, level="EXCEPTION"))

    def __getattr__(self, item):
        return getattr(logger, item)

    @staticmethod
    def _call_info():
        # print(stack())
        caller = getframeinfo(stack()[-1][0])
        return f'{os.path.basename(caller.filename)}:{caller.function}:line {caller.lineno}'

    def _format_args(self, msg="", trace_id="", topic="", call_info=False, level=""):
        """
        当 call_info 为 True 时，才记录行数（因为记录行数，在cpu 跑满时，大概需要 10ms+ 的时间。同时 由于外层封装的原因，行数需要使用反射取出）。
        """
        if not isinstance(msg, (str, dict, list, set)):
            msg = str(msg)

        if not isinstance(msg, dict):
            msg = {'log': msg}

        data = {
            **msg, "trace_id": trace_id, "topic": topic or self._default_topic,
            "level": level, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if call_info:
            data["call_info"] = self._call_info()
        # try:
        json_str = json.dumps(data, ensure_ascii=False, cls=NumpyEncoder)
        return json_str  # 去掉前后括号. 这里是为了兼容 之前的日志。把 msg 添加到本身的日志里面。
        # except TypeError or JSONEncoder:
        #     return str(data).replace("'", '"')
