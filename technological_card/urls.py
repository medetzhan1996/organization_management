from django.urls import path
from . import views

app_name = 'technological_card'
urlpatterns = [
    path('consumable_in_tech_card/list',
         views.ConsumableInTechCardListView.as_view(),
         name="consumable_in_tech_card"),
    path('<int:technological_card>/consumable_in_tech_card/list',
         views.ConsumableInTechCardListView.as_view(),
         name="consumable_in_tech_card"),

    path('technological_card/create',
         views.TechnologicalCardCreateView.as_view(),
         name="technological_card_create"),
    path('technological_card/<int:pk>/update',
         views.TechnologicalCardUpdateView.as_view(),
         name="technological_card_update"),
    path('technological_card/<int:pk>/delete',
         views.TechnologicalCardDeleteView.as_view(),
         name="technological_card_delete"),
    path('consumable/create',
         views.ConsumableCreateView.as_view(),
         name="consumable_create"),
    path('<int:technological_card>/consumable/create',
         views.ConsumableCreateView.as_view(),
         name="consumable_create"),
    path('<int:technological_card>/consumable/list',
         views.ConsumableListView.as_view(),
         name="consumable_list"),
    path('consumable/<int:pk>/update',
         views.ConsumableUpdateView.as_view(),
         name="consumable_update"),
    path('consumable/<int:pk>/delete',
         views.ConsumableDeleteView.as_view(),
         name="consumable_delete"),
    path('consumable/<int:service>/calculate',
         views.ConsumableСalculateView.as_view(),
         name="consumable_calculate"),
    path('consumable/<int:customer>/appointed/service',
         views.ConsumableInAppointedServiceView.as_view(),
         name="consumable_appointed_service"),

]
