from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from posts.views import home_page_view, contact_page_view, about_us_page_view, signup_signin_page_view, business_signup_view


urlpatterns = [
    path('', home_page_view),
    path('home/', home_page_view),
    path('admin/', admin.site.urls),
    path('contact/', contact_page_view),
    path('aboutus/', about_us_page_view),
    path('signin/', signup_signin_page_view),
    path('businesssignup/',business_signup_view)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
