from django.urls import path
from . import views
app_name = 'cashier'
urlpatterns = [
    path('accept/payment/<int:schedule>', views.AcceptPaymentView.as_view(),
         name="accept_payment"),
]
