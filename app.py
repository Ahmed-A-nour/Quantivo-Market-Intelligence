import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Quantivo Intelligence", layout="wide")

# استايل لتنسيق الألوان والخطوط
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; color: #00fbff; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

data_path = os.path.join(os.getcwd(), 'ecommerce_data.csv')

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    st.title("📊 Quantivo | Executive Market Intelligence")
    
    # صف المؤشرات (KPIs)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Gross Revenue", f"${df['Sales'].sum():,.0f}")
    m2.metric("Net Profit", f"${df['Profit'].sum():,.0f}", f"{((df['Profit'].sum()/df['Sales'].sum())*100):.1f}% Margin")
    m3.metric("Global Cities", df['City'].nunique())
    m4.metric("Transactions", f"{len(df):,}")

    # إنشاء التبويبات
    tab1, tab2 = st.tabs(["📍 Market Distribution", "📈 Performance Analytics"])

    with tab1:
        col_left, col_right = st.columns([1.2, 1])
        
        with col_left:
            st.subheader("Regional Profitability")
            map_df = df.groupby(['City', 'Lat', 'Lon']).agg({'Sales':'sum', 'Profit':'sum'}).reset_index()
            fig_map = px.scatter_mapbox(
                map_df, lat="Lat", lon="Lon", size="Sales", color="Profit",
                hover_name="City", size_max=35, zoom=3,
                color_continuous_scale=['#ff0055', '#161b22', '#00fbff'],
                template="plotly_dark", height=600
            )
            fig_map.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

        with col_right:
            st.subheader("Portfolio Composition")
            fig_sun = px.sunburst(
                df, path=['Parent_Category', 'Sub_Category'], values='Sales',
                color='Profit', color_continuous_scale='Viridis',
                template="plotly_dark", height=600
            )
            st.plotly_chart(fig_sun, use_container_width=True)

    with tab2:
        # الشارت الأول: ترند المبيعات
        st.subheader("Sales Trend Over Time")
        trend = df.resample('W', on='Date')['Sales'].sum().reset_index()
        fig_line = px.area(trend, x='Date', y='Sales', template="plotly_dark", height=350)
        fig_line.update_traces(line_color='#00fbff', fillcolor='rgba(0, 251, 255, 0.1)')
        st.plotly_chart(fig_line, use_container_width=True)
        
        # الشارت الثاني: تحليل الأرباح حسب الفئة (جديد)
        st.subheader("Profitability by Category")
        cat_profit = df.groupby('Parent_Category')['Profit'].sum().sort_values().reset_index()
        fig_bar = px.bar(
            cat_profit, x='Profit', y='Parent_Category', orientation='h',
            template="plotly_dark", height=300,
            color='Profit', color_continuous_scale='Bluered_r'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("Data file not found! Please ensure 'ecommerce_data.csv' is in the same directory.")