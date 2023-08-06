
from sparrow_order_lib.es.es_util.field import ESField
from sparrow_order_lib.es.es_util.mock import ESMockDSLInterface
from sparrow_order_lib.es.es_util.exceptions import ESUtilValueException, ESUtilTypeException
from sparrow_order_lib.es.es_util.operators import custom_op
from sparrow_order_lib.es.es_util.constants import ESQueryGroupName


class ESParam(ESMockDSLInterface):
    ''' 描述请求ES的参数 '''

    def __init__(self, field: ESField, op, other):
        self.field = field
        self.other = other
        self.op = op

    def get_dsl(self):
        operator = custom_op(self.op)
        return operator(self.field, self.other)


class ESParamsForOneGroup(ESMockDSLInterface):
    ''' 一组同级别的查询条件, 各个查询条件之间的逻辑关系由上层 group_type 决定 '''

    def __init__(self, espms):
        self.espms = espms

    def get_dsl(self):
        terms = []
        for espm in self.espms:
            if issubclass(espm.__class__, ESMockDSLInterface):
                terms.append(espm.get_dsl())
            else:
                raise ESUtilTypeException(f'excepted {ESMockDSLInterface.__name__}, got {espm.__class__.__name__}')
        if len(terms) == 1:
            return terms[0]
        # TODO: 如何处理同一个 field 在 range 的合并
        return terms


class ESParamGroup(ESMockDSLInterface):
    ''' 将一组查询条件按照一定的逻辑组装在一起 '''
    __query_name = None

    def __new__(cls, *args, **kwargs):
        espm = args[0]
        query_name = kwargs.pop('query_name')

        # 参数是 ESParam 类型, 或者列表参数的每个元素都是 ESParam 或者参数类型是
        if issubclass(espm.__class__, ESMockDSLInterface):
            pass
        else:  # 参数类型有误
            raise ESUtilValueException("ES查询参数类型错误")

        for sub in cls.__subclasses__():
            if getattr(sub, "_" + sub.__name__ + "__query_name") == query_name:
                return object.__new__(sub)

        return super().__new__(cls)

    def __init__(self, espm: ESMockDSLInterface, *, query_name: str = None):

        self.espm = espm
        # self.query_name = query_name

    def get_dsl(self):
        return {self.query_name: self.espm.get_dsl()}

    def add_one_espm(self, es_param):
        if isinstance(self.espm, ESParam):
            self.espm = ESParamsForOneGroup([self.espm, es_param])
        elif isinstance(self.espm, ESParamsForOneGroup):
            self.espm.espms.append(es_param)
            # self.espm.append(es_param)
        else:
            raise ValueError(1)

    @property
    def query_name(self):
        return self.__query_name


class ESParamShouldGroup(ESParamGroup):
    ''' should query '''
    __query_name = ESQueryGroupName.SHOULD

    @property
    def query_name(self):
        return self.__query_name


class ESParamMustGroup(ESParamGroup):
    ''' must query '''
    __query_name = ESQueryGroupName.MUST

    @property
    def query_name(self):
        return self.__query_name


class ESParamMustNotGroup(ESParamGroup):
    '''' must_not query '''
    __query_name = ESQueryGroupName.MUST_NOT

    @property
    def query_name(self):
        return self.__query_name


class ESParamPageGroup(ESMockDSLInterface):
    ''' page Group '''
    __query_name = ESQueryGroupName.PAGINATION

    @property
    def query_name(self):
        return self.__query_name

    def __init__(self, page, page_size):
        self.page = page
        self.page_size = page_size

    def get_dsl(self):
        dsl = {
            'size': self.page_size,
            'from': (self.page - 1) * self.page_size
        }
        return dsl


class ESParamAggsGroup(ESMockDSLInterface):
    ''' aggs '''
    __query_name = ESQueryGroupName.AGGS

    @property
    def query_name(self):
        return self.__query_name
    # TODO: 实现
    pass
