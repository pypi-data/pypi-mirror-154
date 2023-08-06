
from sparrow_order_lib.core.datastructures import ImmutablePropertyClassBase


class DocType(ImmutablePropertyClassBase):
    ORDER = 'order'  # 订单数据


IndexMapping = {
    DocType.ORDER: 'order',
}
