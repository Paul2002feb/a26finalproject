from django.urls import path, include

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='index'),
    path('login',views.TutoringUserSignupView.as_view(), name='login'),
    path('tutorform',views.tutor, name='tutorform'),
    path('requestlist', views.view_requests, name='requestlist'),
    path('tutorsearch', views.search_tutors, name='tutorsearch'),
    # path('tutor_requests', views.tutor_requests, name='tutor_requests')

]