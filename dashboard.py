import streamlit as st
import pandas as pd
import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image

# Page layout
st.set_page_config(page_title='Churn Analysis FinTech', page_icon=':bar_chart:', layout='wide')

df = pd.read_csv('fintech_dashboard.csv')
DATA = {
    'df':df
}

PAGES = {
    'Overall Churn Rate': 'overall_churn_rate',
    'Age Groups': 'age_groups',
    'Housing Status': 'housing_status',
    'Payment Types': 'payment_types',
    'Deposits & Withdrawals': 'deposits_withdrawals',
    'Mobile App Usages': 'app_downloaded',
    'Credit Card Application': 'credit_card_application',
    'Customer Satisfaction': 'customer_satisfaction',
    'Rewards Earned': 'rewards_earned'
}

# Set the default page
DEFAULT_PAGE = 'Overall Churn Rate'

# st.dataframe(df)
st.markdown('Explore the overall churn rate and its variation across customer segments.')
st.title('Churn Analysis FinTech')


# Sidebar with clickable links to page
page = st.sidebar.selectbox('Navigate to:', ['Overall Churn Rate', 'Age Groups', 'Housing Status', 'Payment Types',
                                             'Deposits & Withdrawals', 'Mobile App Usages', 'Credit Card Application',
                                             'Customer Satisfaction', 'Rewards Earned', 'Dashboard'])
image = Image.open('churn-rate.png')
st.sidebar.image(image)

# if page != 'Dashboard':
#     # Display dataset
#     st.subheader('Dataset')
#     st.dataframe(df)


# Calculate the overall churn rate
overall_churn_rate = df['churn'].mean()

# Display overall churn rate
# st.subheader('Overall Churn Rate')
# st.write(f'The overall churn rate in the FinTech company is {overall_churn_rate:.2%}')

# Define layout for each page
if page == 'Dashboard':
    st.subheader('Dashboard')
    # Dashboard Visuals
    overall_churn_rate = df['churn'].mean()
    st.write(f'The overall churn rate is: {overall_churn_rate:.2%}')
    
    age_group_churn_rate = df.groupby('age')['churn'].mean().reset_index()
    fig_age = px.bar(age_group_churn_rate, x='age', y='churn', labels={'churn': 'Churn Rate'}, title='Churn Rate Across Age Groups')
    st.plotly_chart(fig_age)
    
    housing_churn_rate = df.groupby('housing')['churn'].mean().reset_index()
    fig_housing = px.bar(housing_churn_rate, x='housing', y='churn', labels={'churn': 'Churn Rate'}, title='Churn Rate Based on Housing Status')
    st.plotly_chart(fig_housing)
    
    payment_churn_rate = df.groupby('payment_type')['churn'].mean().reset_index()
    fig_payment = px.bar(payment_churn_rate, x='payment_type', y='churn', labels={'churn': 'Churn Rate'}, title='Churn Rate for Different Payment Types')
    st.plotly_chart(fig_payment)
    
    avg_deposits = df.groupby('churn')['deposits'].mean()
    avg_withdrawals = df.groupby('churn')['withdrawal'].mean()
    data = pd.DataFrame({'Churn': avg_deposits.index, 'Avg Deposits': avg_deposits.values, 'Avg Withdrawals': avg_withdrawals.values})
    fig_deposits_withdrawals = px.bar(data, x='Churn', y=['Avg Deposits', 'Avg Withdrawals'],
                                     labels={'value': 'Amount', 'variable': 'Transaction Type'},
                                     title='Average Deposits and Withdrawals for Churned vs. Non-Churned Customers')
    st.plotly_chart(fig_deposits_withdrawals)
    
    app_downloads_churn = df.groupby('churn')['app_downloaded'].value_counts(normalize=True).unstack().reset_index()
    app_downloads_churn = pd.melt(app_downloads_churn, id_vars='churn', value_vars=[0, 1],
                                  value_name='Percentage', var_name='App Downloaded')
    fig_app_downloads = px.bar(app_downloads_churn, x='churn', y='Percentage', color='App Downloaded',
                               labels={'churn': 'Churn Status', 'Percentage': 'Percentage'},
                               title='App Downloads and Churn Rate')
    st.plotly_chart(fig_app_downloads)
    
    credit_card_app_status = df.groupby('churn')['cc_application_begin'].value_counts(normalize=True).unstack().reset_index()
    credit_card_app_status = pd.melt(credit_card_app_status, id_vars='churn', value_vars=[0, 1],
                                     value_name='Percentage', var_name='Application Status')
    fig_credit_card_app = px.bar(credit_card_app_status, x='churn', y='Percentage', color='Application Status',
                                 labels={'churn': 'Churn Status', 'Percentage': 'Percentage'},
                                 title='Credit Card Application Status and Churn Rate')
    st.plotly_chart(fig_credit_card_app)
    
    fig_customer_satisfaction = px.box(df, x='churn', y=['cc_liked', 'cc_disliked'],
                                       labels={'churn': 'Churn Status', 'value': 'Satisfaction Score'},
                                       title='Customer Satisfaction: Likes and Dislikes')
    st.plotly_chart(fig_customer_satisfaction)
    
    fig_rewards_earned = px.histogram(df, x='rewards_earned', color='churn', barmode='overlay',
                                      labels={'churn': 'Churn Status', 'rewards_earned': 'Rewards Earned'},
                                      title='Rewards Earned Distribution')
    st.plotly_chart(fig_rewards_earned)
    
if page == 'Overall Churn Rate':
    st.subheader('Overall Churn Rate')
    # Calculate overall churn rate
    overall_churn_rate = df['churn'].mean()
    st.write(f'The overall churn rate in the FinTech company is: {overall_churn_rate:.2%}')

     # Create a pie chart for the overall churn rate
    churn_count = df['churn'].value_counts()
    fig = px.pie(
        churn_count,
        names=churn_count.index,
        values=churn_count.values,
        labels=['Not Churned', 'Churned'],
        title='Churn Distribution'
    )
    st.plotly_chart(fig)
    st.dataframe(df)
elif page == 'Age Groups':
        # Bar plot showing churn rate across age groups
        age_group_churn_rate = df.groupby('age')['churn'].mean().reset_index()
        fig_age = px.bar(age_group_churn_rate, x='age', y='churn', labels={'churn': 'Churn Rate'}, title='Churn Rate Across Age Groups')
        # Display visualization and dataset below it
        st.plotly_chart(fig_age)

# Page 3: Housing Status
elif page == 'Housing Status':
        # Bar plot showing churn rate based on housing status
        housing_churn_rate = df.groupby('housing')['churn'].mean().reset_index()
        fig_housing = px.bar(housing_churn_rate, x='housing', y='churn', labels={'churn': 'Churn Rate'}, title='Churn Rate Based on Housing Status')
        st.plotly_chart(fig_housing)

# Page 4: Payment Types
elif page == 'Payment Types':
        # Bar plot showing churn rate for different payment types
        payment_churn_rate = df.groupby('payment_type')['churn'].mean().reset_index()
        fig_payment = px.bar(payment_churn_rate, x='payment_type', y='churn', labels={'churn': 'Churn Rate'}, title='Churn Rate for Different Payment Types')
        st.plotly_chart(fig_payment)
    
# Page 5: Deposits & Withdrawals
elif page == 'Deposits & Withdrawals':
        st.subheader('Deposits and Withdrawals Analysis')
        
        # Visualization related to deposits and withdrawals (customize according to your specific question)
        # Example: Bar plot showing average deposits and withdrawals for churned vs. non-churned customers
        avg_deposits = df.groupby('churn')['deposits'].mean()
        avg_withdrawals = df.groupby('churn')['withdrawal'].mean()
        data = pd.DataFrame({'Churn': avg_deposits.index, 'Avg Deposits': avg_deposits.values, 'Avg Withdrawals': avg_withdrawals.values})
        fig_deposits_withdrawals = px.bar(data, x='Churn', y=['Avg Deposits', 'Avg Withdrawals'],
                                        labels={'value': 'Amount', 'variable': 'Transaction Type'},
                                        title='Average Deposits and Withdrawals for Churned vs. Non-Churned Customers')
        st.plotly_chart(fig_deposits_withdrawals)

# Page 6: Mobile Apps Usage
elif page == 'Mobile App Usages':
        st.subheader('Mobile App Usages Analysis')
        
        app_downloads_churn = df.groupby('churn')['app_downloaded'].value_counts(normalize=True).unstack().reset_index()
        app_downloads_churn = pd.melt(app_downloads_churn, id_vars='churn', value_vars=[0, 1],
                                  value_name='Percentage', var_name='App Downloaded')
        fig_grouped_bar = px.bar(app_downloads_churn, x='churn', y='Percentage', color='App Downloaded',
                             labels={'churn': 'Churn Status', 'Percentage': 'Percentage'},
                             title='App Downloads and Churn Rate', barmode='group')
        st.plotly_chart(fig_grouped_bar)
        
# Page 7: Credit Card Application
elif page == 'Credit Card Application':
        st.subheader('Credit Card Application Analysis')
        credit_card_app_status = df.groupby('churn')['cc_application_begin'].value_counts(normalize=True).unstack().reset_index()
        credit_card_app_status = pd.melt(credit_card_app_status, id_vars='churn', value_vars=[0, 1],
                                        value_name='Percentage', var_name='Application Status')
        fig_credit_card_app = px.bar(credit_card_app_status, x='churn', y='Percentage', color='Application Status',
                                    labels={'churn': 'Churn Status', 'Percentage': 'Percentage'},
                                    title='Credit Card Application Status and Churn Rate')
        st.plotly_chart(fig_credit_card_app)
        
# Page 8: Customer Satisfaction
elif page == 'Customer Satisfaction':
        st.subheader("Customer's Overall Experience")
        # Stacked bar plot showing counts of likes and dislikes for each churn status
        customer_satisfaction_counts = df.groupby(['churn', 'cc_liked', 'cc_disliked']).size().reset_index(name='Count')
        color_discrete_map = {'0': 'lightgrey', '1': 'red'}
        fig_customer_satisfaction = px.bar(customer_satisfaction_counts, x='churn', y='Count', color='cc_liked',
                                       labels={'churn': 'Churn Status', 'Count': 'Count'},
                                       title="Customer Satisfaction: Likes and Dislikes",
                                       barmode='stack')
        st.plotly_chart(fig_customer_satisfaction)
        
# Page 9: Rewards Earned
elif page == 'Rewards Earned':
        st.subheader('Reward Points earned by Customers who left the bank.')
        fig_rewards_earned = px.histogram(df, x='rewards_earned', color='churn', barmode='overlay',
                                        labels={'churn': 'Churn Status', 'rewards_earned': 'Rewards Earned'},
                                        title='Rewards Earned Distribution')
        st.plotly_chart(fig_rewards_earned)

