from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from myapp.views import ItemViewSet, home_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import os
from django.conf import settings

# Инициализация DRF роутера
router = DefaultRouter()
router.register(r'items', ItemViewSet)

# Настройка Swagger/Redoc
schema_view = get_schema_view(
    openapi.Info(
        title="MyProject API",
        default_version='v1',
        description="Документация для API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Инициализация Dash приложения
dash_app = dash.Dash(
    __name__,
    server=settings.WSGI_APPLICATION,
    url_base_pathname='/dash/',
    assets_folder=os.path.join(settings.BASE_DIR, 'static', 'dash'),
)

# Функция для получения данных из NocoDB
def get_noco_data():
    api_token = os.getenv("NOCODB_API_TOKEN", "O1RmgUMHz73SXi7Tmbilnu7-lqY3Bc4ZA4FqYhhK")
    table_id = os.getenv("NOCODB_TABLE_ID", "mhk38g2tng1cv63")
    view_id = os.getenv("NOCODB_VIEW_ID", "vwukd5wkscz37nmj")
    url = f"{os.getenv('NOCODB_URL', 'http://nocodb:8080')}/api/v2/tables/{table_id}/records?offset=0&limit=100&viewId={view_id}"
    response = requests.get(url, headers={'xc-token': api_token})
    return response.json().get('list', [])

# Лейаут Dash приложения
dash_app.layout = html.Div([
    html.H1('Данные из NocoDB'),
    dcc.Graph(id='noco-graph'),
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Обновление каждую минуту
        n_intervals=0
    )
])

# Callback для обновления данных
@dash_app.callback(
    Output('noco-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    data = get_noco_data()
    return {
        'data': [{
            'x': [item.get('id') for item in data],
            'y': [item.get('value') for item in data],  # Замените 'value' на ваш столбец
            'type': 'bar'
        }]
    }

# Основные URL паттерны
urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    urlpatterns = [
    path('', views.home, name='home'),
    # другие пути...
]