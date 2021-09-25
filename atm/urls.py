from django.conf.urls import url
from django.urls import path
from atm import views as atm_views

urlpatterns = [
    url('^signup$', atm_views.UserSignUp.as_view({'post': 'create'}), name='create-users'),
    url('^login$', atm_views.Login.as_view({'post': 'create'}), name='log-in'),

    path('atmdetails', atm_views.ATMDetailOperations.as_view({'post': 'create', 'get': 'list'}), name='atm-details'),
    path("retrieveatmdetails/<int:atm_id>", atm_views.ATMDetailOperations.as_view({"get": "retrieve"}),
         name="retrieve-atmdetails"),
    path("updateatmdetails/<int:atm_id>", atm_views.ATMDetailOperations.as_view({"put": "update"}), name="update-atmdetails"),

]
