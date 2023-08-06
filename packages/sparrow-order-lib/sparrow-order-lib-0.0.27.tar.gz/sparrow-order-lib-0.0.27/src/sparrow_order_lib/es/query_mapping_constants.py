from sparrow_order_lib.es.constants import DocType


# 存放各文档的查询 mapping
QUERY_MAPPING = {
    # 订单数据
    DocType.ORDER: {
        'phone': [
            {
                'path': 'user.user_name',
            },
            {
                'path': 'shipping_address.phone'
            }
        ],
        'distribute_id': {
            'path': 'distributes.id'
        },
        'distribute_number': {
            'path': 'distributes.number'
        }
    }
}


QUERY_MAPPING_SPECIAL_FUNC = {
    # 查询的特殊函数
}
