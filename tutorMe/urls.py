"""tutorMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from home import views
from django.conf.urls.static import static

urlpatterns = [
    path('',include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('notification/', views.notification_page,name='notification'),
    path('schedule/', views.schedule_page,name='schedule'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/course/', views.search_courses, name='courses'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    # path('tutor_requests/', views.tutor_requests, name='tutor_requests')

]
