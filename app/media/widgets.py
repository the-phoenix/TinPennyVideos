from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminURLFieldWidget
from django.utils.translation import gettext_lazy as _
from django.utils.html import smart_urlquote

from .utils import s3_to_http_schema
from .validators import s3_path_validator


class AdminS3PathFieldWidget(AdminURLFieldWidget):
    template_name = 'admin/widgets/s3-path.html'

    def __init__(self, attrs=None):
        super().__init__(
            attrs={'class': 'vS3PathField', **(attrs or {})},
            validator_class=lambda : s3_path_validator
        )

    def get_context(self, name, value, attrs):
        try:
            self.validator(value if value else '')
            url_valid = True
        except ValidationError:
            url_valid = False
        context = super().get_context(name, value, attrs)
        context['current_label'] = _('Currently:')
        context['change_label'] = _('Change:')
        context['url_valid'] = url_valid

        if url_valid is True:
            http_urls = s3_to_http_schema(value, True)

            if http_urls["distributed"] is not None:
                context['distributed_label'] = _('Distributed:')
                context['distributed_value'] = smart_urlquote(http_urls["distributed"])

            context['widget']['href'] = smart_urlquote(http_urls["pre_signed"])

        return context
