import streamlit as st
from snowflake_query import get_query_history, get_warehouse_utilization
from llm_analyzer import generate_query_insights
from snowflake_query import estimate_cost_savings

query_df = get_query_history()
wh_df = get_warehouse_utilization()
estimated_savings = estimate_cost_savings(query_df, wh_df)

st.set_page_config(page_title="💸 Snowflake Cost Insight Bot", layout="wide")

st.title("💸 Snowflake Cost Insight Bot")
st.markdown("Get AI-generated insights on your Snowflake costs and usage.")

st.subheader("Top Expensive Queries")
query_df = get_query_history()
st.dataframe(query_df)

if st.button("Generate AI Insight"):
    with st.spinner("Generating suggestions..."):
        insights = generate_query_insights(query_df, estimated_savings)

        st.success("✅ Insight Generated!")
        st.markdown(insights)

st.subheader("Warehouse Utilization")
wh_df = get_warehouse_utilization()
st.dataframe(wh_df)
