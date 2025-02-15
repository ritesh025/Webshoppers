from django.urls import path
from myapp import views

urlpatterns=[
    path('',views.index, name="index"),
    path('contact', views.contact,name="contact"),
    path('about', views.about,name="about"),
    path('checkout/', views.checkout ,name="Checkout"),
    path('payment/', views.payment ,name="payment"),
    path('succes/', views.succes ,name="succes"),
    path('profile/', views.profile ,name="profile"),
    # path('handlerequest/', views.handlerequest ,name="HandleRequest"),
    # path('paypal/', include('paypal.standard.ipn.urls')),
]
