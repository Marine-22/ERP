from erp.apps.resources.models import UserProfile

def user_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        profile = None
    return {'profile':profile}