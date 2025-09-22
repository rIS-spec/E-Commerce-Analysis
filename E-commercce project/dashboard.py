import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def perform_analytics_and_visualize(file_path):
    """
    Performs data analysis and visualization on e-commerce transaction data
    and displays it using a Streamlit app.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Load the CSV file into a DataFrame
        df_transactions = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found.")
        st.info("Please ensure the CSV file is in the same directory as this script and try again.")
        return
    
    # --- Data Cleaning and Preparation ---
    df_transactions.columns = [col.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_') for col in df_transactions.columns]
    df_transactions['Transaction_Date'] = pd.to_datetime(df_transactions['Transaction_Date'])

    st.title("🛍️ E-commerce Analytics Dashboard")
    st.markdown("A comprehensive look at key metrics and trends from transaction data.")

    # --- Key Performance Indicators (KPIs) ---
    st.header("Key Performance Indicators 📊")

    # 1. Total Revenue
    total_revenue = df_transactions['Purchase_Amount'].sum()
    
    # 2. Average Purchase Value
    avg_purchase_value = df_transactions['Purchase_Amount'].mean()
    
    # 3. Number of Transactions
    total_transactions = df_transactions.shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Average Purchase Value", f"${avg_purchase_value:,.2f}")
    col3.metric("Total Transactions", f"{total_transactions:,}")

    st.divider()

    # --- Visualizations ---
    
    # Row 1: Revenue by Category & Top Countries
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Product Category 📦")
        revenue_by_category = df_transactions.groupby('Product_Category')['Purchase_Amount'].sum().sort_values(ascending=False).reset_index()
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.barplot(x='Purchase_Amount', y='Product_Category', data=revenue_by_category, ax=ax)
        ax.set_title('Revenue by Product Category')
        ax.set_xlabel('Total Revenue ($)')
        ax.set_ylabel('Product Category')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Top 5 Countries by Revenue 🌎")
        top_countries_revenue = df_transactions.groupby('Country')['Purchase_Amount'].sum().nlargest(5).reset_index()
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.barplot(x='Country', y='Purchase_Amount', data=top_countries_revenue, ax=ax)
        ax.set_title('Top 5 Countries by Revenue')
        ax.set_xlabel('Country')
        ax.set_ylabel('Total Revenue ($)')
        st.pyplot(fig)

    st.divider()

    # Row 2: Monthly Revenue & Age Group Revenue
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Monthly Revenue Trend 📈")
        monthly_revenue = df_transactions.set_index('Transaction_Date').resample('ME')['Purchase_Amount'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(12, 7))
        sns.lineplot(x='Transaction_Date', y='Purchase_Amount', data=monthly_revenue, ax=ax)
        ax.set_title('Monthly Revenue Trend')
        ax.set_ylabel('Total Revenue ($)')
        ax.set_xlabel('Date')
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Revenue by Age Group 🧑‍🦳")
        bins = [0, 19, 29, 39, 49, float('inf')]
        labels = ['Below 20', '20s', '30s', '40s', '50+']
        df_transactions['Age_Group'] = pd.cut(df_transactions['Age'], bins=bins, labels=labels, right=True, include_lowest=True)
        revenue_by_age_group = df_transactions.groupby('Age_Group')['Purchase_Amount'].sum().reindex(labels).reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Age_Group', y='Purchase_Amount', data=revenue_by_age_group, ax=ax)
        ax.set_title('Revenue by Age Group')
        ax.set_ylabel('Total Revenue ($)')
        ax.set_xlabel('Age Group')
        st.pyplot(fig)
            
    st.divider()

    # --- Detailed Tables and Insights ---
    st.header("Detailed Analysis 🔍")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Customer Insights", "Revenue Metrics", "Product & Market", "Advanced Analytics"])

    with tab1:
        st.subheader("Top 10 Customers by Spending 💰")
        top_customers = df_transactions.groupby('User_Name')['Purchase_Amount'].sum().nlargest(10).reset_index()
        st.dataframe(top_customers, use_container_width=True)
        
        st.subheader("Most Frequent Shoppers 🏃")
        most_frequent_shoppers = df_transactions['User_Name'].value_counts().nlargest(10).reset_index()
        most_frequent_shoppers.columns = ['User_Name', 'Order_Count']
        st.dataframe(most_frequent_shoppers, use_container_width=True)
        
        st.subheader("Average Age of Customers 🎂")
        avg_age = df_transactions['Age'].mean()
        st.metric(label="Average Customer Age", value=f"{avg_age:.2f} years")
        
    with tab2:
        st.subheader("Daily Average Sales 📆")
        daily_avg_sales = df_transactions.set_index('Transaction_Date').resample('D')['Purchase_Amount'].mean().round(2).reset_index()
        daily_avg_sales.columns = ['Day', 'avg_daily_sales']
        fig, ax = plt.subplots(figsize=(12, 7))
        sns.lineplot(x='Day', y='avg_daily_sales', data=daily_avg_sales, ax=ax)
        ax.set_title('Daily Average Sales')
        ax.set_ylabel('Average Sales ($)')
        ax.set_xlabel('Date')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        st.subheader("Revenue by Payment Method 💵")
        revenue_by_payment_method = df_transactions.groupby('Payment_Method')['Purchase_Amount'].sum().sort_values(ascending=False).reset_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Payment_Method', y='Purchase_Amount', data=revenue_by_payment_method, ax=ax)
        ax.set_title('Revenue Contribution by Payment Method')
        ax.set_ylabel('Total Revenue ($)')
        ax.set_xlabel('Payment Method')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)
        
        st.subheader("Peak Shopping Day 🏆")
        peak_shopping_day = df_transactions.groupby('Transaction_Date')['Purchase_Amount'].sum().nlargest(1).reset_index()
        st.metric(label="Date with Highest Revenue", value=peak_shopping_day['Transaction_Date'].iloc[0].strftime("%B %d, %Y"))
        st.metric(label="Revenue on Peak Day", value=f"${peak_shopping_day['Purchase_Amount'].iloc[0]:,.2f}")
    
    with tab3:
        st.subheader("Percentage Share of Each Country in Revenue (%) 🗺️")
        country_revenue = df_transactions.groupby('Country')['Purchase_Amount'].sum()
        total_revenue = country_revenue.sum()
        country_revenue_percentage = (country_revenue / total_revenue * 100).round(2).reset_index()
        country_revenue_percentage.columns = ['Country', 'Revenue_Percentage']
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.pie(country_revenue_percentage['Revenue_Percentage'], labels=country_revenue_percentage['Country'], autopct='%1.1f%%', startangle=90)
        ax.set_title('Percentage Share of Each Country in Revenue')
        st.pyplot(fig)
        
        st.subheader("Top 5 Product Categories per Country 🗺️")
        df_transactions['Country'] = df_transactions['Country'].astype('category')
        ranked_sales = df_transactions.groupby(['Country', 'Product_Category'])['Purchase_Amount'].sum().reset_index()
        ranked_sales['rank_in_country'] = ranked_sales.groupby('Country')['Purchase_Amount'].rank(method='first', ascending=False)
        top_categories_by_country = ranked_sales[ranked_sales['rank_in_country'] <= 5]
        top_categories_by_country = top_categories_by_country.sort_values(by=['Country', 'Purchase_Amount'], ascending=[True, False])
        st.dataframe(top_categories_by_country, use_container_width=True)

    with tab4:
        st.subheader("Monthly Revenue Growth Rate 🚀")
        monthly_revenue_trend = df_transactions.set_index('Transaction_Date').resample('ME')['Purchase_Amount'].sum()
        monthly_revenue_df = monthly_revenue_trend.reset_index()
        monthly_revenue_df['Previous_Month_Revenue'] = monthly_revenue_df['Purchase_Amount'].shift(1)
        monthly_revenue_df['Growth_Rate_Percentage'] = (monthly_revenue_df['Purchase_Amount'] - monthly_revenue_df['Previous_Month_Revenue']) / monthly_revenue_df['Previous_Month_Revenue'] * 100
        fig, ax = plt.subplots(figsize=(12, 7))
        sns.lineplot(x='Transaction_Date', y='Growth_Rate_Percentage', data=monthly_revenue_df.dropna(), ax=ax)
        ax.set_title('Month-over-Month Revenue Growth Rate (%)')
        ax.set_ylabel('Growth Rate (%)')
        ax.set_xlabel('Date')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        st.subheader("Product Affinity Analysis (Top 5 Co-purchased Categories) 🤝")
        most_popular_categories = df_transactions['Product_Category'].value_counts().nlargest(5).reset_index()
        most_popular_categories.columns = ['Product_Category', 'Transaction_Count']
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Product_Category', y='Transaction_Count', data=most_popular_categories, ax=ax)
        ax.set_title('Most Popular Product Categories by Transaction Count')
        ax.set_ylabel('Transaction Count')
        ax.set_xlabel('Product Category')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(fig)

        st.subheader("Customer Lifetime Value (CLV) by Country 💖")
        clv_by_country = df_transactions.groupby('Country').agg(
            total_revenue=('Purchase_Amount', 'sum'),
            unique_customers=('User_Name', 'nunique')
        ).reset_index()
        clv_by_country['CLV'] = clv_by_country['total_revenue'] / clv_by_country['unique_customers']
        clv_by_country = clv_by_country.sort_values('CLV', ascending=False)
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Country', y='CLV', data=clv_by_country, ax=ax)
        ax.set_title('Customer Lifetime Value (CLV) by Country')
        ax.set_ylabel('Average CLV ($)')
        ax.set_xlabel('Country')
        st.pyplot(fig)

if __name__ == "__main__":
    perform_analytics_and_visualize('ecommerce_transactions.csv')