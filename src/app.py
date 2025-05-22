import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
from database.db_manager import DatabaseManager
from dotenv import load_dotenv
import os
import pathlib

# Load environment variables
load_dotenv()

# Initialize database with absolute path
current_dir = pathlib.Path(__file__).parent.parent.absolute()
db_path = os.path.join(current_dir, 'data', 'finance.db')
db_url = f'sqlite:///{db_path}'
db = DatabaseManager(db_url)

# Page configuration
st.set_page_config(
    page_title="Personal Finance Manager",
    page_icon="💰",
    layout="wide"
)

def main():
    st.title("Personal Finance Manager 💰")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Add Transaction", "View Transactions", "Reports"]
    )
    
    # Temporary user_id (replace with actual user authentication)
    user_id = 1
    
    if page == "Dashboard":
        show_dashboard(user_id)
    elif page == "Add Transaction":
        show_add_transaction(user_id)
    elif page == "View Transactions":
        show_transactions(user_id)
    else:
        show_reports(user_id)

def show_dashboard(user_id):
    st.header("Financial Dashboard")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )
    
    # Get summary data
    summary = db.get_category_summary(user_id, start_date, end_date)
    
    # Calculate totals
    total_income = sum(summary['income'].values())
    total_expenses = sum(summary['expense'].values())
    net_savings = total_income - total_expenses
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}", "")
    col2.metric("Total Expenses", f"${total_expenses:,.2f}", "")
    col3.metric("Net Savings", f"${net_savings:,.2f}", 
                f"{(net_savings/total_income*100 if total_income else 0):.1f}%")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Income Distribution")
        if summary['income']:
            fig = px.pie(
                values=list(summary['income'].values()),
                names=list(summary['income'].keys()),
                title="Income by Category"
            )
            st.plotly_chart(fig)
        else:
            st.info("No income data available for selected period")
    
    with col2:
        st.subheader("Expense Distribution")
        if summary['expense']:
            fig = px.pie(
                values=list(summary['expense'].values()),
                names=list(summary['expense'].keys()),
                title="Expenses by Category"
            )
            st.plotly_chart(fig)
        else:
            st.info("No expense data available for selected period")

def show_add_transaction(user_id):
    st.header("Add New Transaction")
    
    with st.form("transaction_form"):
        # Transaction type
        transaction_type = st.selectbox(
            "Transaction Type",
            ["expense", "income"]
        )
        
        # Amount
        amount = st.number_input(
            "Amount ($)",
            min_value=0.01,
            format="%f"
        )
        
        # Category
        if transaction_type == "expense":
            categories = ["Food", "Transport", "Utilities", "Entertainment", "Other"]
        else:
            categories = ["Salary", "Investment", "Freelance", "Gift", "Other"]
        
        category = st.selectbox("Category", categories)
        
        # Note
        note = st.text_area("Note (Optional)")
        
        # Date
        date = st.date_input("Date", datetime.now())
        
        # Submit button
        submitted = st.form_submit_button("Add Transaction")
        
        if submitted:
            try:
                db.add_transaction(
                    user_id=user_id,
                    type=transaction_type,
                    category=category,
                    amount=amount,
                    note=note,
                    date=date
                )
                st.success("Transaction added successfully!")
            except Exception as e:
                st.error(f"Error adding transaction: {str(e)}")

def show_transactions(user_id):
    st.header("Transaction History")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        start_date = st.date_input(
            "Start Date",
            datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            datetime.now()
        )
    with col3:
        transaction_type = st.selectbox(
            "Type",
            ["All", "Income", "Expense"]
        )
    
    # Get transactions
    transactions = db.get_transactions(user_id, start_date, end_date)
    
    if transaction_type != "All":
        transactions = [t for t in transactions if t.type.lower() == transaction_type.lower()]
    
    if transactions:
        # Convert to DataFrame for display
        df = pd.DataFrame([
            {
                "Date": t.date,
                "Type": t.type.capitalize(),
                "Category": t.category,
                "Amount": t.amount,
                "Note": t.note or ""
            }
            for t in transactions
        ])
        
        st.dataframe(df)
        
        # Download button
        if st.button("Export to CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "transactions.csv",
                "text/csv"
            )
    else:
        st.info("No transactions found for the selected period")

def show_reports(user_id):
    st.header("Financial Reports")
    
    # Time period selector
    period = st.selectbox(
        "Select Period",
        ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year"]
    )
    
    # Calculate date range
    end_date = datetime.now()
    if period == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    elif period == "Last 3 Months":
        start_date = end_date - timedelta(days=90)
    elif period == "Last 6 Months":
        start_date = end_date - timedelta(days=180)
    else:
        start_date = end_date - timedelta(days=365)
    
    # Get transactions
    transactions = db.get_transactions(user_id, start_date, end_date)
    
    if transactions:
        # Create DataFrame
        df = pd.DataFrame([
            {
                "Date": t.date,
                "Type": t.type,
                "Amount": t.amount if t.type == "income" else -t.amount
            }
            for t in transactions
        ])
        
        # Group by date
        daily_totals = df.groupby("Date")["Amount"].sum().reset_index()
        
        # Create cumulative chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_totals["Date"],
            y=daily_totals["Amount"].cumsum(),
            mode='lines+markers',
            name='Net Worth'
        ))
        
        fig.update_layout(
            title="Net Worth Over Time",
            xaxis_title="Date",
            yaxis_title="Amount ($)"
        )
        
        st.plotly_chart(fig)
        
        # Monthly breakdown
        st.subheader("Monthly Summary")
        monthly = df.set_index("Date").resample("M")["Amount"].sum()
        st.bar_chart(monthly)
        
    else:
        st.info("No data available for the selected period")

if __name__ == "__main__":
    main() 