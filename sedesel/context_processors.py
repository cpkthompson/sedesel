import datetime


def site(request):
    return {
        'current_year': datetime.datetime.now().year
    }
