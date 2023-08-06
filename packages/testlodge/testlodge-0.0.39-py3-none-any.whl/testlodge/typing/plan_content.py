from typing import List
from typing import TypedDict

from testlodge.typing.custom_field import CustomFieldJSON
from testlodge.typing.shared import DateTimeStr
from testlodge.typing.shared import Pagination
from testlodge.typing.shared import UserID


class PlanContentJSON(TypedDict):

    id: int
    title: str
    content: str
    position: int
    plan_id: int
    last_saved_by_id: UserID
    created_at: DateTimeStr
    updated_at: DateTimeStr
    custom_fields: List[CustomFieldJSON]


class PlanContentListJSON(TypedDict):

    pagination: Pagination
    steps: List[PlanContentJSON]
