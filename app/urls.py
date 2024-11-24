from django.urls import path
from . import views
from django.urls import path

urlpatterns = [

    path('', views.home, name='home'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('informacije/', views.informacije, name='informacije'),

    path('pretraga/', views.pretraga, name='pretraga'),
    path('artikl/<str:turbo_maker_oe_no>/', views.ArtiklInfo, name='artikl_info'),

    path('informacije/kako-funkcionise-turbo/', views.kako_funkcionise_turbo, name='kako-funkcionise-turbo'),
    path('informacije/simptomi-kvara-turbine/', views.simptomi_kvara_turbine, name='simptomi-kvara-turbine'),
    path('informacije/zasto-se-kvari-turbina/', views.zasto_se_kvari_turbina, name='zasto-se-kvari-turbina'),
    path('informacije/zasto-turbina-trosi-ulje/', views.zasto_turbina_trosi_ulje, name='zasto-turbina-trosi-ulje'),
    path('informacije/instrukcije-za-montazu/', views.instrukcije_za_montazu, name='instrukcije-za-montazu'),

]
