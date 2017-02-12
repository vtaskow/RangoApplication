"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import warnings
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rango import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from registration.backends.simple.views import RegistrationView
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user=None):
        return '/rango/'


# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above


urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', views.index, name='index'),
                  # Any URLs starting with rango are handled by the rango application
                  url(r'^rango/', include('rango.urls')),
                  url(r'^accounts/password/change/$', auth_views.password_change,
                      {'post_change_redirect': reverse_lazy('auth_password_change_done'),
                       'template_name': 'registration/password_change_form.html'}, name='auth_password_change'),
                  url(r'^password/change/done/$', auth_views.password_change_done, name='auth_password_change_done'),
                  url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
                  # Any URLs starting with accounts are handled by the registration-redux application
                  url(r'^accounts/', include('registration.backends.simple.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
