from django.urls import path
from .views import add_expense, get_balances

urlpatterns = [
    path('add-expense/', add_expense, name='add_expense'),
    path('get-balances/<str:user_id>/', get_balances, name='get_balances'),
    
]
