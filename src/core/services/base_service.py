from rest_framework.exceptions import ValidationError


class BaseService:
    def _ensure_not_duplicate(self, exists: bool, message: str):
        if exists:
            raise ValidationError(message)
