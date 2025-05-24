import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pymysql as sql

# Set Streamlit page config
st.set_page_config(page_title="PhonePe", layout="wide")

# Database connection
conn = sql.connect(host="127.0.0.1", user="root", password="Selva765799#")
cursor = conn.cursor()
cursor.execute("USE PhonePe_project")

# Sidebar Menu
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Explore Data", "Insights"],
                           icons=["house", "bar-chart-line", "search"])

# Home page
if selected == "Home":

    st.markdown("# :red[Data Visualization and Exploration]")
    st.markdown("## :red[A User-Friendly Tool Using Streamlit and Plotly]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.markdown("### :red[Technologies used:] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, Plotly")
        st.markdown("### :red[Overview:] Visualize PhonePe Pulse data and gain insights on transactions, insurance, and top regions by activity.")

# Explore data page
if selected == "Explore Data":
        @st.cache_data
        def load_data():
            cursor.execute("SELECT * FROM Aggregated_Transaction")
            result = cursor.fetchall()
            return pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
        
        df = load_data()

        years = sorted(df['Year'].unique())
        quarters = sorted(df['Quarter'].unique())
        col1, col2 = st.columns([5,3])

        with st.sidebar:
                selected_type = st.selectbox("Type", ["Payments", "Insurance"], key="report")    
                selected_year = st.selectbox("Select Year", years)
                selected_quarter = st.selectbox("Select Quarter",quarters)
                
        # Payments
        if selected_type == "Payments":
            
            with col1:
                st.markdown("### :red[Overall Data - Payments]")
                cursor.execute(f"""
                    SELECT state, SUM(Transaction_count), SUM(Transaction_amount), 
                        ROUND(SUM(Transaction_amount) / SUM(Transaction_count), 2)
                    FROM map_transaction 
                    WHERE year = {selected_year} AND quarter = {selected_quarter} 
                    GROUP BY state ORDER BY state;
                """)
            
                df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'All Transactions', 'Total Payment', 'Avg.Transaction'])

                df1['Total Payment Value(cr)'] = df1['Total Payment'] / 10**7
                df1['Total Payment Value'] = df1['Total Payment Value(cr)'].apply(lambda x: f"₹{x:,.2f} Cr")
                df1['Avg.Transaction Value'] = df1['Avg.Transaction'].apply(lambda x: f"₹{x:,.2f}")

                fig = px.choropleth(
                    df1,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total Payment Value(cr)',
                    color_continuous_scale='reds',
                    hover_data={'All Transactions': True, 'Total Payment Value': True, 'Avg.Transaction Value': True,'Total Payment Value(cr)':False}
                )

                fig.update_layout(coloraxis_colorbar=dict(title="Payment (₹ Crores)"))
                fig.update_geos(visible=False, projection_type="mercator", center={"lat": 22, "lon": 80}, lonaxis={"range": [66, 100]}, lataxis={"range": [6, 38]})
                st.plotly_chart(fig, use_container_width=True)

            with col2:

                cursor.execute(f"""
                    SELECT SUM(Transaction_count), SUM(Transaction_amount) 
                    FROM aggregated_transaction 
                    WHERE year = {selected_year} AND quarter = {selected_quarter};
                """)
                result = cursor.fetchone()

                total_transactions = float(result[0]) if result[0] else 0
                total_amount = float(result[1]) if result[1] else 0
                avg_transaction_value = round(total_amount / total_transactions, 2) if total_transactions else 0
                total_amount_crore = total_amount / 10**7

                st.subheader("Transactions")
                st.text("All PhonePe transactions (UPI + Cards + Wallets)")
                st.markdown(f"<h3>{total_transactions:,.0f}</h3>", unsafe_allow_html=True)

                col3, col4 = st.columns(2)
                col3.metric("Total Payment Value", f"₹{total_amount_crore:,.0f} Cr")
                col4.metric("Avg. Transaction Value", f"₹{avg_transaction_value:,.0f}")

                cursor.execute(f"""
                    SELECT Transaction_type, SUM(Transaction_amount) 
                    FROM aggregated_transaction 
                    WHERE year = {selected_year} AND quarter = {selected_quarter} 
                    GROUP BY Transaction_type;
                """)
                categories_data = cursor.fetchall()

                st.subheader("Categories")
                for category, amount in categories_data:
                    st.write(f"{category}: ₹{amount / 10**7:,.0f} Cr")

    # Insurance
        elif selected_type == "Insurance":
            st.markdown("### :red[Overall Data - Insurance]")

            if selected_year in [2018, 2019] or selected_year in [2020] and selected_quarter in [1]:
                st.markdown(f"#### Sorry, No Data to Display for {selected_year} Qtr {selected_quarter}.")
            else:
                col1, col2 = st.columns([4, 4])

                with col1:

                    cursor.execute(f"""
                        SELECT state, SUM(Transaction_count), SUM(Transaction_amount),
                            ROUND(SUM(Transaction_amount) / SUM(Transaction_count), 2)
                        FROM map_insurance 
                        WHERE year = {selected_year} AND quarter = {selected_quarter} 
                        GROUP BY state ORDER BY state;
                    """)
                    df1 = pd.DataFrame(cursor.fetchall(), columns=['State', "Insurance Policies(No's)", 'Total Premium', 'Avg Premium'])

                    df1['Total Premium(cr)'] = df1['Total Premium'] / 10**7
                    df1['Total Premium Value'] = df1['Total Premium(cr)'].apply(lambda x: f"₹{x:,.2f} Cr")
                    df1['Avg Premium Value'] = df1['Avg Premium'].apply(lambda x: f"₹{x:,.2f}")

                    fig = px.choropleth(
                        df1,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total Premium(cr)',
                        color_continuous_scale='reds',
                        hover_data={"Insurance Policies(No's)": True, 'Total Premium Value': True, 'Avg Premium Value': True, 'Total Premium(cr)': False}
                    )
                    fig.update_layout(coloraxis_colorbar=dict(title="Premium (₹ Crores)"))
                    fig.update_geos(visible=False, projection_type="mercator", center={"lat": 22, "lon": 80}, lonaxis={"range": [66, 100]}, lataxis={"range": [6, 38]})
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    cursor.execute(f"""
                        SELECT SUM(Insurance_count), SUM(Insurance_amount),
                            ROUND(SUM(Insurance_amount) / SUM(Insurance_count), 2)
                        FROM aggregated_insurance 
                        WHERE year = {selected_year} AND quarter = {selected_quarter};
                    """)
                    result = cursor.fetchone()

                    total_insurance = float(result[0]) if result[0] else 0
                    total_premium = float(result[1]) if result[1] else 0
                    avg_premium = float(result[2]) if result[2] else 0
                    total_premium_crore = total_premium / 10**7

                    st.subheader("Insurance")
                    st.text("All India Insurance Policies Purchased (Nos.)")
                    st.markdown(f"<h3>{total_insurance:,.0f}</h3>", unsafe_allow_html=True)

                    col3, col4 = st.columns(2)
                    col3.metric("Total Premium Value", f"₹{total_premium_crore:,.0f} Cr")
                    col4.metric("Avg. Premium Value", f"₹{avg_premium:,.0f}")

# Insights
if selected == "Insights":
    Insights_type = st.sidebar.selectbox("Select Insights", ["Transaction Insights", "Insurance Insights","User Insights"])

    # Transaction Insights
    if Insights_type == "Transaction Insights":
        @st.cache_data
        def load_data():
            cursor.execute("SELECT * FROM Aggregated_Transaction")
            result = cursor.fetchall()
            return pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

        df = load_data()

        st.title("📊 Multi-State Transaction Dynamics on PhonePe")
        selected_states = st.sidebar.multiselect("Select States", df["State"].unique(), default=["Karnataka", "Maharashtra"])
        selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
        selected_type = st.sidebar.selectbox("Select Transaction Type", df["Transaction_type"].unique())

        filtered = df[(df["State"].isin(selected_states)) & 
                      (df["Year"] == selected_year) & 
                      (df["Transaction_type"] == selected_type)].copy()
        filtered["Amount_Crore"] = filtered["Transaction_amount"] / 10**7

        st.markdown(f"### Summary: {', '.join(selected_states)} | {selected_year} | {selected_type}")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 💰 Transaction Amount (₹ Cr) by Quarter")
            fig_amount = px.bar(filtered, x="Quarter", y="Amount_Crore", color="State", barmode="group", text_auto=True)
            st.plotly_chart(fig_amount, use_container_width=True)

        with col2:
            st.markdown("#### 🔄 Transaction Count by Quarter")
            fig_count = px.line(filtered, x="Quarter", y="Transaction_count", color="State", markers=True)
            st.plotly_chart(fig_count, use_container_width=True)

    # Insurance Insights
    if Insights_type == "Insurance Insights":
        @st.cache_data
        def load_data():
            agg = pd.read_sql("SELECT * FROM aggregated_insurance", conn)
            map_ = pd.read_sql("SELECT * FROM map_insurance", conn)
            top = pd.read_sql("SELECT * FROM top_insurance", conn)
            return agg, map_, top

        df_agg, df_map, df_top = load_data()

        st.title("📈 Insurance Penetration & Growth Potential")

        states = df_agg['State'].dropna().unique().tolist()
        years = sorted(df_agg['Year'].unique())
        quarters = sorted(df_agg['Quarter'].unique())

        with st.sidebar:
            selected_states = st.multiselect("Select State(s)", states, default=["Karnataka", "Maharashtra"])
            selected_year = st.selectbox("Select Year", years)
            selected_quarter = st.selectbox("Select Quarter", quarters)

        filtered_agg = df_agg[
            (df_agg['State'].isin(selected_states)) &
            (df_agg['Year'] == selected_year) &
            (df_agg['Quarter'] == selected_quarter)
        ]

        # Convert to Crores
        filtered_agg['Insurance_amount_Cr'] = (filtered_agg['Insurance_amount'] / 1e7).round(2)

        # Summary
        st.subheader(f"📊 Summary for {', '.join(selected_states)} - Q{selected_quarter}, {selected_year}")
        col1, col2 = st.columns(2)
        col1.metric("🧾 Insurance Transactions", int(filtered_agg['Insurance_count'].sum()))
        col2.metric("💰 Total Amount (₹ Cr)", filtered_agg['Insurance_amount_Cr'].sum())

        # Bar Chart: Insurance Amount by State
        st.markdown("#### Insurance Transaction Amount by State")
        fig_amt = px.bar(
            filtered_agg,
            x="State",
            y="Insurance_amount_Cr",
            color="State",
            text_auto=True,
            labels={"Insurance_amount_Cr": "Amount (₹ Cr)"}
        )
        st.plotly_chart(fig_amt, use_container_width=True)

        # Line Chart: Insurance Growth Over Time
        st.markdown("#### 📈 Insurance Growth Over Time")
        growth_data = df_agg[df_agg['State'].isin(selected_states)]
        growth_data['Insurance_amount_Cr'] = growth_data['Insurance_amount'] / 1e7
        growth_data['Year_Quarter'] = growth_data['Year'].astype(str) + " Q" + growth_data['Quarter'].astype(str)

        fig_growth = px.line(
            growth_data,
            x='Year_Quarter',
            y='Insurance_amount_Cr',
            color='State',
            markers=True,
            labels={"Insurance_amount_Cr": "Amount (₹ Cr)", "Year_Quarter": "Time"}
        )
        st.plotly_chart(fig_growth, use_container_width=True)

        # District-level insights
        st.markdown("#### 📍 District-Level Insurance Distribution")
        map_filtered = df_map[
            (df_map["State"].isin(selected_states)) &
            (df_map["Year"] == selected_year) &
            (df_map["Quarter"] == selected_quarter)
        ]
        map_filtered["Transaction_amount_Cr"] = map_filtered["Transaction_amount"] / 1e7

        fig_district = px.bar(
            map_filtered,
            x="District",
            y="Transaction_amount_Cr",
            color="State",
            text_auto=True,
            labels={"Transaction_amount_Cr": "Amount (₹ Cr)"}
        )
        st.plotly_chart(fig_district, use_container_width=True)

    #USER INSIGHTS
    if Insights_type == "User Insights":
        @st.cache_data
        def load_data():
            cursor.execute("""SELECT State,District,SUM(Registered_User) AS total_users,SUM(App_Opens) AS total_app_opens FROM Map_User
                GROUP BY State, District
                ORDER BY total_app_opens DESC;""")
            result = cursor.fetchall()
            return pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])

        df = load_data()

        df['total_users'] = pd.to_numeric(df['total_users'], errors='coerce')
        df['total_app_opens'] = pd.to_numeric(df['total_app_opens'], errors='coerce')

        states = st.sidebar.multiselect("Select States", df["State"].unique(), default=df["State"].unique())

        filtered_df = df[df["State"].isin(states)]

        st.title("📊 User Engagement and Growth Strategy")
        st.markdown("### App Opens and User Registrations by District")

        # Bubble chart: App Opens vs Registered Users
        fig = px.scatter(
        filtered_df,
        x="total_users",
        y="total_app_opens",
        size="total_app_opens",
        color="State",
        hover_name="District",
        title="User Registrations vs App Opens by District",
        labels={"total_users": "Registered Users", "total_app_opens": "App Opens"},
    )
        st.plotly_chart(fig, use_container_width=True)

        # Top 10 districts table
        st.markdown("### 🔝 Top 10 Districts by App Opens")
        top10_df = filtered_df.sort_values(by="total_app_opens", ascending=False).head(10)
        st.dataframe(top10_df.reset_index(drop=True))
                
# Close DB connection
cursor.close()
conn.close()