from app.models.case import ClinicalCase
from app.models.checklist import ChecklistItem
from app.models.comment import Comment
from app.services.ai.base import AIProvider


class MockAIProvider(AIProvider):
    name = "mock"

    def generate_case_summary(
        self,
        case: ClinicalCase,
        comments: list[Comment],
        checklist_items: list[ChecklistItem],
    ) -> str:
        done_count = sum(1 for item in checklist_items if item.is_done)
        total_count = len(checklist_items)
        last_comments = comments[-3:]
        comments_text = "\n".join(f"- {comment.text}" for comment in last_comments) or "- Комментариев пока нет"

        return (
            f"Краткая сводка по кейсу #{case.id}: {case.title}\n\n"
            f"Статус: {case.status.value}\n"
            f"Приоритет: {case.priority.value}\n"
            f"Код пациента/кейса: {case.patient_code or 'не указан'}\n\n"
            f"Описание: {case.description}\n\n"
            f"Прогресс чек-листа: {done_count}/{total_count} выполнено.\n\n"
            f"Последние комментарии:\n{comments_text}\n\n"
            "Рекомендация: проверить невыполненные пункты чек-листа, "
            "зафиксировать замечания в комментариях и перевести кейс на ревью, "
            "если критичных проблем не найдено."
        )
