from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
app_name = 'RPG'


class MyHackedView(auth_views.PasswordResetView):
    success_url = reverse_lazy('RPG:password_reset_done')


urlpatterns = [
    path('', views.start_page, name='start_page'),
    path("use_crystal/<str:crystal>", views.use_crystal, name='use_crystal'),
    path("crystal/", views.crystal, name='crystal'),
    path('<int:page_number>', views.content, name='content'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', MyHackedView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('RPG:password_reset_complete')),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
]
