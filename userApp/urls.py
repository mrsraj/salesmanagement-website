from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginpage, name="loginpage"),
    path("registration/", views.registerpage),
    path("savedata/", views.savedata),
    path("pswdverify/", views.pswdverify),
    path("dashboard/",views.dashboardpage),
    path("CustData/",views.CustomerData),
    path("Add_Customer/",views.CustomerPage),
    path("Add_Service/",views.Add_Service),
    path("logout/",views.logout),
    path("About/",views.AboutFun),
    path("Showclient/",views.ShowClient),
    path("ShowSupplier/",views.ShowSupplier),
    
    path('delete/<int:Id>/', views.delete),
    
    path('DetailsPage.html/',views.detailsPage),
    path('dashboard/<str:type>/',views.apifunction),
    path('payment/',views.PaymentPage),
    path('payment/',views.PaymentForm),
]
 