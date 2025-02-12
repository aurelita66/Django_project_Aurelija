from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_nm'),
    path('autos/', views.get_autos, name='autos-all'),
    path('autos/<int:auto_id>', views.get_one_auto, name='auto-one'),
    path('orders/', views.UzsakymasListView.as_view(), name='orders-all'),
    path('orders/<int:pk>', views.UzsakymasDetailView.as_view(), name='order-one'),
    path('search/', views.search, name='search_nm'),
    path('myorders/', views.OrdersByUserListView.as_view(), name='my-orders'),
    path('register/', views.register_user, name='register'),
    path('profile/', views.get_user_profile, name='user-profile'),

]
