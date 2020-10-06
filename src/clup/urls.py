from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from posts.views import *


urlpatterns = [
    path('', home_page_view),
    path('home/', home_page_view),
    path('admin/', admin.site.urls),
    path('contact_us/', contact_page_view),
    path('about_us/', about_us_page_view),
    path('signin/', signup_signin_page_view),
    path('signup/', customer_signup_view),
    path('business_sign_in/',business_login_view),
    path('business_sign_up/',business_signup_view),
    path('reset/', forgot_password_view),
    path('control_panel/', control_panel_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
