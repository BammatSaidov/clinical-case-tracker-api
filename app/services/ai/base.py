from abc import ABC, abstractmethod

from app.models.case import ClinicalCase
from app.models.checklist import ChecklistItem
from app.models.comment import Comment


class AIProvider(ABC):
    name: str

    @abstractmethod
    def generate_case_summary(
        self,
        case: ClinicalCase,
        comments: list[Comment],
        checklist_items: list[ChecklistItem],
    ) -> str:
        raise NotImplementedError
