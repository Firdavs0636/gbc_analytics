import os
from flask import Flask, render_template_string
from supabase import create_client

app = Flask(__name__)

# 1. Setup Supabase Connection
SUPABASE_URL = "https://maawfesxlfgetjvdybob.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hYXdmZXN4bGZnZXRqdmR5Ym9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNTI5NTUsImV4cCI6MjA5MTcyODk1NX0.a9T7TK2Ys6vHRsFvn2OVEO3N6GLG3htjW7VkjskFKeQ"  # Use Anon key for the dashboard
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# st.set_page_config(page_title="RetailCRM Order Dashboard", layout="wide")
#
# st.title("🚀 Order Analytics Dashboard")
# st.markdown("Data fetched from **Supabase**, originally from **RetailCRM**.")
#
#
# # 2. Fetch Data
# def get_data():
#     response = supabase.table("orders").select("*").execute()
#     return pd.DataFrame(response.data)
#
#
# df = get_data()
#
# if not df.empty:
#     # 3. Data Cleaning
#     df['created_at'] = pd.to_datetime(df['created_at'])
#
#     # 4. Display Metrics
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Orders", len(df))
#     col2.metric("Total Revenue", f"{df['total_sum'].sum():,.0f} ₸")
#     col3.metric("Avg Order Value", f"{df['total_sum'].mean():,.0f} ₸")
#
#     # 5. Build Chart
#     st.subheader("Sales Over Time")
#     # Grouping by date
#     daily_sales = df.groupby(df['created_at'].dt.date)['total_sum'].sum().reset_index()
#     fig = px.line(daily_sales, x='created_at', y='total_sum',
#                   title='Daily Revenue (₸)', markers=True)
#     st.plotly_chart(fig, use_container_width=True)
#
#     # 6. Show Table
#     st.subheader("Recent Orders")
#     st.dataframe(df[['first_name', 'last_name', 'city', 'total_sum', 'status']], use_container_width=True)
# else:
#     st.error("No data found in Supabase!")

@app.route('/')
def index():
    try:
        # 2. Fetch Data
        response = supabase.table("orders").select("*").execute()
        orders = response.data

        # 3. Simple HTML Dashboard
        html_template = """
        <html>
            <head>
                <title>RetailCRM Dashboard</title>
                <style>
                    body { font-family: sans-serif; padding: 40px; background: #f4f7f6; }
                    .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th, td { text-align: left; padding: 12px; border-bottom: 1px solid #eee; }
                    th { background: #3b82f6; color: white; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>🚀 Order Analytics</h1>
                    <p>Total Orders synced: {{ orders|length }}</p>
                    <table>
                        <tr>
                            <th>Name</th>
                            <th>City</th>
                            <th>Total Sum</th>
                            <th>Status</th>
                        </tr>
                        {% for o in orders %}
                        <tr>
                            <td>{{ o.first_name }} {{ o.last_name }}</td>
                            <td>{{ o.city }}</td>
                            <td>{{ o.total_sum }} ₸</td>
                            <td>{{ o.status }}</td>
                        </tr>
                        {% endfor %}
                    </table>
                </div>
            </body>
        </html>
        """
        return render_template_string(html_template, orders=orders)
    except Exception as e:
        return f"Error connecting to Supabase: {str(e)}"

