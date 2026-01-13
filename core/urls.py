from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('menu/', views.menu_principal_view, name='menu_principal'),
    path('alta-nino/', views.alta_nino_view, name='alta_nino'),
    path('modificar-nino/', views.modificar_nino_view, name='modificar_nino'),
    path('eliminar-nino/', views.eliminar_nino_view, name='eliminar_nino'),
    path('narracion/', views.narracion_view, name='narracion'),
    path('finalizar-lectura/', views.finalizar_lectura_view, name='finalizar_lectura'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('cuentos/', views.lista_cuentos_view, name='lista_cuentos'),
    path('narracion/<int:cuento_id>/', views.narracion_view, name='narracion'),
    path('resumen-lectura/', views.resumen_lectura_view, name='resumen_lectura'),
    path('registro/', views.registro_view, name='registro'),
   
]