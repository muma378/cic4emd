# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
from django.utils import timezone

def validate_not_past(value):
    tz_now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
    if tz_now - value > timedelta(seconds=300):    # if the error is less than 5 minute
        raise ValidationError(
            ugettext_lazy(u'发布日期不能早于当前'),
            params={'value':value})