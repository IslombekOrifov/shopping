from django.conf import settings

from accounts.models import CustomUser


def get_ckeditor_upload_path(request):
    if request.user.role != CustomUser.CHOICE_ROLE[0][0] and request.user.role != CustomUser.CHOICE_ROLE[-1][0]:
        path_upload = f"{request.user.company.name}/products/"
    elif request.user.role == CustomUser.CHOICE_ROLE[-1][0]:
        path_upload = f"blog/posts/"
    return path_upload


