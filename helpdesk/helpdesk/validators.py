from pathlib import Path
from django.core.exceptions import ValidationError

ALLOWED_UPLOAD_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"}
MAX_UPLOAD_SIZE = 5 * 1024 * 1024


def validate_attachment(file_obj):
    suffix = Path(file_obj.name).suffix.lower()
    if suffix not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ValidationError("Only JPG, PNG, PDF, DOC, and DOCX files are allowed.")
    if file_obj.size > MAX_UPLOAD_SIZE:
        raise ValidationError("Attachment size must not exceed 5 MB.")
