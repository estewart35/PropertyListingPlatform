from .models import Profile

def user_profile(request):
    if request.user.is_authenticated:
        try:
            user_profile = request.user.profile
        except Profile.DoesNotExist:
            user_profile = None
    else:
        user_profile = None

    return {'user_profile': user_profile}
