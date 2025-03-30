import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import http.client
import json


def load_data():
    conn = http.client.HTTPSConnection("app.nocodb.com")
    
   
    api_token = "O1RmgUMHz73SXi7Tmbilnu7-lqY3Bc4ZA4FqYhhK"
    table_id = "mhk38g2tng1cv63"
    view_id = "vwukd5wkscz37nmj"
    
    headers = {'xc-token': api_token}
    url = f"/api/v2/tables/{table_id}/records?offset=0&limit=100&where=&viewId={view_id}"
    
    try:
        conn.request("GET", url, headers=headers)
        res = conn.getresponse()
        
        if res.status == 200:
            data = json.loads(res.read().decode("utf-8"))
            df = pd.DataFrame(data["list"])
            
            # Автоматическое преобразование числовых колонок
            for col in df.columns:
                if pd.api.types.is_string_dtype(df[col]):
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except:
                        pass
            
            return df
        else:
            print(f"Ошибка {res.status}: {res.reason}")
            return pd.DataFrame()  # Возвращаем пустой DataFrame при ошибке
            
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# Инициализация Dash-приложения
app = dash.Dash(__name__)
df = load_data()

# Создание графиков на основе данных
def create_charts(df):
    charts = []
    
    if not df.empty:
        # 1. Определяем числовые и категориальные колонки
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # 2. Столбчатая диаграмма для первой числовой колонки
        if len(numeric_cols) > 0:
            first_numeric = numeric_cols[0]
            fig = px.bar(df, x=categorical_cols[0] if len(categorical_cols) > 0 else df.index, 
                        y=first_numeric, title=f'Распределение {first_numeric}')
            charts.append(dcc.Graph(figure=fig))
        
        # 3. Круговая диаграмма для первой категориальной колонки
        if len(categorical_cols) > 0:
            first_categorical = categorical_cols[0]
            if df[first_categorical].nunique() < 20:
                fig = px.pie(df, names=first_categorical, title=f'Распределение по {first_categorical}')
                charts.append(dcc.Graph(figure=fig))
        
        # 4. Точечная диаграмма для связи между двумя числовыми колонками
        if len(numeric_cols) >= 2:
            x_col, y_col = numeric_cols[0], numeric_cols[1]
            color_col = categorical_cols[0] if len(categorical_cols) > 0 else None
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                            title=f'Зависимость {x_col} и {y_col}')
            charts.append(dcc.Graph(figure=fig))
    
    else:
        # Заглушка, если данные не загрузились
        charts.append(html.Div("Данные не загружены. Проверьте подключение к NocoDB."))
    
    return charts

# Лейаут приложения
app.layout = html.Div([
    html.H1("Дашборд данных из NocoDB", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    html.Div([
        html.H3("Первые 5 строк данных:", style={'marginTop': '20px'}),
        html.Table(
            [html.Tr([html.Th(col) for col in df.columns])] +
            [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) 
             for i in range(min(5, len(df)))]
        ) if not df.empty else html.Div("Нет данных для отображения", style={'color': 'red'})
    ], style={'margin': '20px', 'padding': '15px', 'border': '1px solid #eee', 'borderRadius': '5px'}),
    
    html.Div(create_charts(df), id='charts-container'),
    
    dcc.Interval(
        id='interval-component',
        interval=300*1000,  # Обновление каждые 5 минут
        n_intervals=0
    )
], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1200px', 'margin': '0 auto'})

# Callback для обновления данных
@app.callback(
    dash.dependencies.Output('charts-container', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_charts(n):
    df = load_data()
    return create_charts(df)

if __name__ == '__main__':
    app.run(debug=True, port=8050)