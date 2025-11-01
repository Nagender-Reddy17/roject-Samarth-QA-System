import streamlit as st
import pandas as pd

# -----------------------------
# Load Datasets
# -----------------------------
@st.cache_data
def load_data():
    rainfall = pd.read_csv("rainfall_statewise.csv")
    crops = pd.read_csv("crop_production_statewise.csv")
    return rainfall, crops

rainfall_df, crops_df = load_data()

st.title("🌾 Project Samarth – Agricultural Q&A System")
st.caption("Built for intelligent insights from Government datasets (IMD + MoA&FW)")

# -----------------------------
# Show raw data (optional)
# -----------------------------
with st.expander("📂 View Raw Datasets"):
    st.subheader("Rainfall Data (IMD)")
    st.dataframe(rainfall_df)
    st.subheader("Crop Production Data (MoA&FW)")
    st.dataframe(crops_df)

# -----------------------------
# User input (Q&A Interface)
# -----------------------------
st.header("🔍 Ask a Question")
query = st.text_input("Type your question (e.g., 'Compare rainfall in Maharashtra and Karnataka for last 3 years')")

if query:
    query = query.lower()
    
    # -----------------------------
    # Case 1: Compare Rainfall between two states
    # -----------------------------
    if "compare" in query and "rainfall" in query:
        # Try to extract states
        states = [s for s in rainfall_df["State"].unique() if s.lower() in query]
        if len(states) >= 2:
            s1, s2 = states[:2]
            st.subheader(f"🌧️ Comparing Rainfall: {s1} vs {s2}")
            
            data1 = rainfall_df[rainfall_df["State"] == s1].sort_values("Year", ascending=False).head(3)
            data2 = rainfall_df[rainfall_df["State"] == s2].sort_values("Year", ascending=False).head(3)
            
            avg1 = round(data1["Annual_Rainfall_mm"].mean(), 2)
            avg2 = round(data2["Annual_Rainfall_mm"].mean(), 2)
            
            st.write(f"- **Average Rainfall in {s1} (last 3 yrs):** {avg1} mm")
            st.write(f"- **Average Rainfall in {s2} (last 3 yrs):** {avg2} mm")
            st.line_chart(data=pd.concat([data1, data2]).pivot(index="Year", columns="State", values="Annual_Rainfall_mm"))
            
            st.caption("📊 Source: Simulated IMD dataset (data.gov.in)")
    
    # -----------------------------
    # Case 2: Top crops by production
    # -----------------------------
    elif "top" in query and "crop" in query:
        states = [s for s in crops_df["State"].unique() if s.lower() in query]
        if states:
            state = states[0]
            latest_year = crops_df[crops_df["State"] == state]["Year"].max()
            df_latest = crops_df[(crops_df["State"] == state) & (crops_df["Year"] == latest_year)]
            top_crops = df_latest.sort_values("Production_Tonnes", ascending=False).head(3)
            
            st.subheader(f"🌾 Top Crops in {state} ({latest_year})")
            st.dataframe(top_crops[["Crop", "Production_Tonnes"]])
            st.bar_chart(data=top_crops.set_index("Crop")["Production_Tonnes"])
            
            st.caption("📊 Source: Simulated MoA&FW dataset (data.gov.in)")
    
    # -----------------------------
    # Case 3: Production trend
    # -----------------------------
    elif "trend" in query or "over last" in query:
        crops_mentioned = [c for c in crops_df["Crop"].unique() if c.lower() in query]
        if crops_mentioned:
            crop = crops_mentioned[0]
            df_crop = crops_df[crops_df["Crop"] == crop].groupby(["Year"]).sum().reset_index()
            st.subheader(f"📈 Production Trend for {crop} (All India)")
            st.line_chart(df_crop.set_index("Year")["Production_Tonnes"])
            st.caption("📊 Source: Simulated MoA&FW dataset (data.gov.in)")
    
    # -----------------------------
    # Fallback
    # -----------------------------
    else:
        st.warning("⚠️ Sorry, I couldn’t parse your question. Try:")
        st.markdown("""
        - "Compare rainfall in Maharashtra and Karnataka for last 3 years"
        - "Show top crops in Punjab"
        - "Show trend of Sugarcane production"
        """)

