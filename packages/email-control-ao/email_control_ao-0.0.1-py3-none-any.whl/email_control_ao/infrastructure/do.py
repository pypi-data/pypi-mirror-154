from typing import List, Optional
from dataclasses import dataclass
from ddd_objects.infrastructure.do import BaseDO

@dataclass
class EmailInfoDO(BaseDO):
    sender: str
    receiver: str
    subject: str
    content: Optional[str]=None
    html_content: Optional[str]=None
    from_alias: Optional[str]=None
    reply_address: Optional[str]=None
    reply_address_alias: Optional[str]=None
    reply_to_address: str=False
    address_type: str=1
    click_trace: str='1'