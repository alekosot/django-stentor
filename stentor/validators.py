from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from stentor import settings as stentor_conf


def validate_template_choice(template_name):
    if template_name not in stentor_conf.TEMPLATES:
        raise ValidationError(
            _('%(template_name)s is not a choice given in the available '
              'templates'),
            params={'template_name': template_name})
