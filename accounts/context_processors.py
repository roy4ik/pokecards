from django.contrib.auth.forms import AuthenticationForm    
from .models import Profile
def get_login_form(request):
    context = {'login_form': AuthenticationForm()}
    # if request.user.is_authenticated:
    #     context.update({'profile': Profile.objects.get(user=request.user)})
    return context