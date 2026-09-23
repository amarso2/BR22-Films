from django.core.files.storage import FileSystemStorage
from django.conf import settings

class BR22MediaStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs["location"] = settings.MEDIA_ROOT
        kwargs["base_url"] = settings.MEDIA_URL
        super().__init__(*args, **kwargs)

media_storage = BR22MediaStorage()