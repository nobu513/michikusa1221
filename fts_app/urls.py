
from django.urls import path
from .views import homefunc, rankfunc, detail_func, gofunc, kebaruja_ja, kebaruja_ko

urlpatterns = [
    path('', homefunc, name='home'),
    path('detail/<int:pk>', detail_func, name='detail'),
    path('rank/', rankfunc, name='rank'),
    path('gofunc/', gofunc, name='gofunc'),
    # path('sosiku/', sosiku, name="sosiku"),
    path('kebaruja_ja/', kebaruja_ja, name='kebaruja_ja'),
    path('kebaruja_ko/', kebaruja_ko, name='kebaruja_ko'),
   
]
