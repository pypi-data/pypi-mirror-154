'''
定义 ES 各类 field, 实现逻辑关系行为
'''
from abc import ABC

from sparrow_order_lib.es.es_util.constants import ESFieldType
from sparrow_order_lib.es.es_util.exceptions import ESUtilParamException, ESUtilValueException
from sparrow_order_lib.es.es_util.operators import FieldOperators


class ESField(ABC, FieldOperators):

    def __new__(cls, **kwargs):
        if 'type' not in kwargs:
            raise ESUtilParamException("缺少关键字参数 type")
        if 'path' not in kwargs:
            raise ESUtilParamException("缺少关键字参数 path")

        type = kwargs['type']
        for sc in ESField.__subclasses__():
            if sc.type == type:
                return object.__new__(sc)
        else:
            raise ESUtilValueException(f"无法解析的字段类型: {type}")

    def __init__(self, *, path, type):
        self.path = path
        # self.type = type


class TextField(ESField):
    type = ESFieldType.TEXT


class DateTimeField(ESField):
    type = ESFieldType.DATETIME


class BooleanField(ESField):
    type = ESFieldType.BOOLEAN


class KeywordField(ESField):
    type = ESFieldType.KEYWORD


class NestedField(ESField):
    type = ESFieldType.NESTED


class ObjectField(ESField):
    type = ESFieldType.OBJECT


class IntegerField(ESField):
    type = ESFieldType.INTEGER
