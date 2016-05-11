from datetime import datetime, timedelta

from django.utils import timezone


def tz_now():
	return timezone.make_aware(datetime.now(), timezone.get_default_timezone())
