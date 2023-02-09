from django.db.models import Func

class Round2(Func):
    function = "ROUND"
    arity = 2

