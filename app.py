import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')

file = st.file_uploader('Upload a csv file')

def load_overall_analysis():
    st.title("Overall Analysis")
    total = round(df['amount'].sum())

    #max amount funding in startup
    max_funding = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0]
    #min amount funding in startup
    min_funding = df.groupby('startup')['amount'].sum().sort_values(ascending=True).head(1).values[0]
    #Avg amount funding in startup
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    #total funded startup
    total_funded_startup = df['startup'].nunique()

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.metric('Total',str(total)+ "Cr")
    with col2:
        st.metric('Max_Funding',str(max_funding)+ "Cr")
    with col3:
        st.metric('Min_Funding',str(min_funding)+ "Cr")
    with col4:
        st.metric('Avg_Funding',str(round(avg_funding))+ "Cr")
    with col5:
        st.metric('Total_Funded_Startup',str(total_funded_startup))


def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 invsestments of investors
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)


    #biggest investments
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Most Biggest Investments')
        st.dataframe(big_series)
        fig, ax =plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum()
        st.subheader('Sectors invested in')

        fig1, ax1 =plt.subplots()
        ax1.pie(vertical_series,labels = vertical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)

    with col3:
        big_stage_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Most Biggest Investments stage wise')
        st.dataframe(big_stage_series)
        fig2, ax2 =plt.subplots()
        ax2.bar(big_stage_series.index,big_stage_series.values)

        st.pyplot(fig2)

    with col4:
        vertical_city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Sectors invested in cities')

        fig3, ax3 =plt.subplots()
        ax3.pie(vertical_city_series,labels = vertical_city_series.index,autopct="%0.01f%%")

        st.pyplot(fig3)

    df['year']=df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY Investment')
   
    fig4, ax4 =plt.subplots()
    ax4.plot(year_series.index,year_series.values)

    st.pyplot(fig4)

if file is not None:
    df = pd.read_csv(file)
    df['date'] = pd.to_datetime(df['date'],errors='coerce')
    st.sidebar.title("Startup Funding Analysis")
    option = st.sidebar.selectbox('Select One',['Overall Analysis','StartUp','Investor']) 

    if option=='Overall Analysis':
        btn0 = st.sidebar.button("Show Overall Analysis")
        if btn0:
            load_overall_analysis()

    elif option=='StartUp':
        st.sidebar.selectbox('Select StartUp',sorted(df['Startup Name'].unique().tolist()))
        btn1 = st.sidebar.button("Find Startup Details")
        st.title("StartUp Analysis")
    else:
        selected_investor = st.sidebar.selectbox('Select investors',sorted(set(df['investors'].str.split(',').sum())))
        btn2 = st.sidebar.button("Find Investors Details")
        st.title('Investor Analysis')
        if btn2:
            load_investor_details(selected_investor)
        

# if file is not None:
#     df = pd.read_csv(file)
#     st.sidebar.title("Batsman Runs Analysis")
#     st.title('complete analysis of batsman')
#     st.dataframe(df)
#     option = st.sidebar.selectbox('select agg func want to do',['max','min'])
#     if option=='max':
        
    



