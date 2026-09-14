
import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Prediction")
st.write("Enter the product details to predict sales:")

Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
Product_Id_char = st.selectbox("Product ID Character", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16)
Product_Type_Category = st.selectbox("Product Type Category", ["Perishables", "Non Perishables"])

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

if st.button("Predict Sales"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data)
    if response.status_code == 200:
        prediction = response.json()["Sales"]
        st.success(f"Predicted Sales: {prediction}")
    else:
        st.error("Failed to make prediction. Please try again.")
st.subheader("Batch Prediction")
uploaded_file = st.file_uploader("Upload a CSV file for batch prediction", type=["csv"])
if uploaded_file is not None:
    if st.button("Predict Sales (Batch)"):
        files = {"file": uploaded_file}
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})
        if response.status_code == 200:
            results = response.json()
            st.success("Predictionss Complete")

            try:
              if isinstance(results, list):
                df = pd.DataFrame(results)
              elif isinstance(results, dict):
                if all(not isinstance(v, (list, dict)) for v in results.values()):
                  df = pd.DataFramce([results])
                else:
                  df = pd.DataFramce(results)
              else:
                  df = pd.DataFramce({"Result": [results]})
              st.dataframe(df, use_container_width=True)

            except Exception as e:
              st.error(f"Error displaying results: {e}")
              st.json(results)
        else:
            st.error("Failed to make batch prediction. Please try again.")
