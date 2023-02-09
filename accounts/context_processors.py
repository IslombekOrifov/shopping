from .forms import UserLogForm

def log_form_for_base(request):
    if  not request.user.is_authenticated:
        login_form = UserLogForm()
        register_form = UserLogForm()
        return {'login_form': login_form, "register_form": register_form}
    else:
        return {'logined': 'user is logined'}