# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Report(models.Model):
    created = models.DateField(auto_now=True)
    file_path = models.CharField(max_length=256)
