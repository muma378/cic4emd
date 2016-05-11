# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy
from django.utils import timezone
from .common import tz_now

def validate_not_past(value):
    if tz_now() - value > timedelta(seconds=300):    # if the delayls is less than 5 minute
        raise ValidationError(
            ugettext_lazy(u'发布日期不能早于当前'),
            params={'value':value})
