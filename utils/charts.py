import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional


COLORS = {
    'IDC': '#2196F3',
    'HQ': '#FF9800',
    'PRD': '#FF5252',
    'STG': '#FFB74D',
    'DEV': '#4CAF50',
    '정상': '#00C853',
    '장애': '#FF5252',
    '점검': '#FF9800',
}

CHART_LAYOUT = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E0E0E0'),
    height=400,
)


def create_location_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    if df.empty:
        return None

    counts = df['location'].value_counts().reset_index()
    counts.columns = ['location', 'count']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=counts['location'],
        y=counts['count'],
        marker=dict(color=[COLORS.get(loc, '#888') for loc in counts['location']]),
        text=counts['count'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>서버 수: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title='설치위치별 서버 수',
        xaxis_title='설치위치',
        yaxis_title='서버 수',
        **CHART_LAYOUT
    )
    return fig


def create_env_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    if df.empty:
        return None

    counts = df['env'].value_counts().reindex(['PRD', 'STG', 'DEV']).fillna(0).reset_index()
    counts.columns = ['env', 'count']

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=counts['env'],
        values=counts['count'],
        hole=0.4,
        marker=dict(colors=[COLORS.get(e, '#888') for e in counts['env']]),
        hovertemplate='<b>%{label}</b><br>서버 수: %{value}<br>비율: %{percent}<extra></extra>'
    ))

    fig.update_layout(
        title='운영등급별 서버 분포',
        **CHART_LAYOUT
    )
    return fig


def create_status_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    if df.empty:
        return None

    counts = df['status'].value_counts().reindex(['정상', '장애', '점검']).fillna(0).reset_index()
    counts.columns = ['status', 'count']

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=counts['status'],
        y=counts['count'],
        marker=dict(color=[COLORS.get(s, '#888') for s in counts['status']]),
        text=counts['count'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>서버 수: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title='운영상태별 서버 분포',
        xaxis_title='상태',
        yaxis_title='서버 수',
        **CHART_LAYOUT
    )
    return fig


def create_location_env_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    if df.empty:
        return None

    pivot = df.groupby(['location', 'env']).size().reset_index(name='count')

    fig = go.Figure()
    for env in ['PRD', 'STG', 'DEV']:
        env_data = pivot[pivot['env'] == env]
        fig.add_trace(go.Bar(
            x=env_data['location'],
            y=env_data['count'],
            name=env,
            marker=dict(color=COLORS.get(env, '#888')),
            text=env_data['count'],
            textposition='auto',
            hovertemplate=f'<b>%{{x}}</b><br>{env}: %{{y}}<extra></extra>'
        ))

    fig.update_layout(
        title='설치위치 x 운영등급 분포',
        xaxis_title='설치위치',
        yaxis_title='서버 수',
        barmode='group',
        **CHART_LAYOUT
    )
    return fig
