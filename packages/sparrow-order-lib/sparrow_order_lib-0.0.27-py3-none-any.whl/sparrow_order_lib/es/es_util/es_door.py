'''
ES 查询组件对外提供的接口
希望能够通过配置实现以下格式的调用:
    door = ESDoor(some_doc_type, condition_1=value_1, condition_2=value_2...)
    res = door.main()  # 即可查询结果
'''
from sparrow_order_lib.es.es_util.constants import ES_QUERY_PAGE_SIZE_DEFAULT
from sparrow_order_lib.es.es_util.in_query_param import InQueryParam
from sparrow_order_lib.es.es_util.es_query_util import ESQueryUtil
from sparrow_order_lib.es.es_util.es_builder import ESBuilder

from sparrow_order_lib.core.datastructures import ImmutableDict


class ESDoor(object):
    '''  '''

    def __init__(self, query_type: str, **kwargs):
        self.doc_type = query_type
        self.query_kwargs = kwargs
        try:
            self.page = kwargs.pop('page')
        except KeyError:
            self.page = 1
        try:
            self.page_size = kwargs.pop('page_size')
        except KeyError:
            self.page_size = ES_QUERY_PAGE_SIZE_DEFAULT

        self.__kwargs = ImmutableDict(kwargs)
        self.__query_params = None
        self.__es_params = None
        self.__es_query_util = None

        self.get_cached_dsl()
        self.format_in_params()
        self.format_es_params()

    def get_cached_dsl(self):
        # 获取缓存的 dsl
        pass

    @property
    def es_query_util(self) -> ESQueryUtil:
        if self.__es_query_util is None:
            self.__es_query_util = ESQueryUtil(self.doc_type)
        return self.__es_query_util

    @property
    def es_params(self):
        return self.__es_params

    def main(self):
        ''' 对外提供统一接口, 负责查询数据 '''
        builder = ESBuilder(index=self.doc_type)
        for query_group in self.__es_params:
            builder.addQueryGroup(query_group)
        builder.addQueryGroup(self.es_query_util.get_page_param_group(self.page, self.page_size))

        result = builder.executeQuery()

        count = result['hits']['total']['value']
        items = result['hits']['hits']

        return {'count': count, 'data': items}

    def format_in_params(self):
        self.__query_params = []
        for in_param_key, in_param_value in self.__kwargs.items():
            inpm = InQueryParam(in_param_key, in_param_value)
            self.__query_params.append(inpm)

    def format_es_params(self):
        self.__es_params = []
        for inpm_obj in self.__query_params:
            espm = self.es_query_util.get_es_query_param(inpm_obj)
            self.__es_params.append(espm)
