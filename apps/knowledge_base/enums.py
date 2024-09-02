from django.utils.translation import gettext as _


class DocumentStatus(object):
    TRAINING = "Training"
    READY = "Ready"
    ERROR = "Error"

    CHOICE = (
        (TRAINING, _("Training")),
        (READY, _("Ready")),
        (ERROR, _("Error")),
    )


class SourceType(object):
    LOCAL = "local_file"
    WEB = "web_link"
    CUSTOM = "custom_text"

    CHOICE = (
        (LOCAL, _("Local File")),
        (WEB, _("Web Link")),
        (CUSTOM, _("Custom Text")),
    )
