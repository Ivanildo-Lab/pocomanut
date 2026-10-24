"""
URL configuration for pocomanut project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# pocomanut/urls.py (VERSÃO CORRIGIDA E FINAL)

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rotas da API REST
    path('api/', include('core.urls')),

    # Rotas da Aplicação Web (Frontend)
    path('', include('core.web_urls', namespace='web')),
]

# Rota /media/ INCONDICIONAL (o helper static() nao serve nada com DEBUG=False ->
# imagens/fotos dariam 404 em producao; correcao igual ao commit 7d9aa25 do e-metalurgicaservicos)
re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})