from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from dj_rest_auth import views
from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="cleaning.kg",
        default_version='v1',
        description="Open API for cleaning.kg",
        contact=openapi.Contact(email="sultanbek9899@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(("backend.apps.api.urls", "backend.apps.api"), namespace="api")),

    # login in rest-auth page
    path('api/auth/', include('rest_framework.urls')),
    path('api/rest-auth/', include('dj_rest_auth.urls')),
    path('api/rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    # password reset with email
    path('api/rest-auth/password/reset/confirm/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # verification email after registration
    re_path(r'registration/account-confirm-email/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(r'registration/account-confirm-email/(?P<key>[-:\w]+)/', VerifyEmailView.as_view(),
            name='account_confirm_email'),
    # api documentation
    path('', schema_view.with_ui('swagger',
                                 cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
