from main.models import TempFile
import datetime


def delete_temp_files():
    for temp in TempFile.objects.all():
        time_delta = datetime.datetime.now() - temp.created_at
        if ((time_delta.total_seconds() / 60) > 5):
            temp.delete()
