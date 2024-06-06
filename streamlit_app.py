import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Farmer Information Dashboard", page_icon="🌾", layout="wide")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

# Sidebar for file upload and filters
st.sidebar.title("Settings")
st.sidebar.image("logo1.jpg", width=150)

# File upload button
uploaded_file = st.sidebar.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    # Read the Excel file
    df = pd.read_excel(uploaded_file)
    
    # Print out the column names to debug
    st.sidebar.write("Columns in DataFrame:", df.columns.tolist())
    
    # Main content
    st.title("Farmer Information Dashboard")
    
    try:
        # Display table with selected columns
        st.subheader("Farmers Information Table")
        st.dataframe(df[['Farmer ID', 'Name of the  Farmer', 'Mobile No', 'Village', 'Total Area Holding (Ha)']])

        # Interactive Filters
        crop_filter = st.sidebar.multiselect("Select Crops", options=df['Production area for crop'].unique(), default=df['Production area for crop'].unique())
        gender_filter = st.sidebar.radio("Select Gender", options=['All', 'M', 'F'], index=0)
        
        # Filter data based on sidebar inputs
        filtered_df = df[df['Production area for crop'].isin(crop_filter)]
        if gender_filter != 'All':
            filtered_df = filtered_df[filtered_df['Gender M/F'] == gender_filter]

        # Drop down to select village
        villages = filtered_df['Village'].unique()
        selected_village = st.sidebar.selectbox('Select Village', villages)

        # Filter data by selected village
        village_data = filtered_df[filtered_df['Village'] == selected_village]

        # Main layout
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            st.image("logo1.jpg", width=100)
            st.metric("Farmers Count", len(df))
            st.metric("Average Temperature", "34°C")
            st.metric("Location", "Kadapa")

        with col2:
            st.markdown("### Production area for crop")
            st.bar_chart(village_data['Production area for crop'].value_counts())

            st.markdown("### Production count by Village")
            st.bar_chart(filtered_df['Village'].value_counts())

            st.markdown("### Production by Crop")
            st.bar_chart(village_data['Production area for crop'].value_counts())

        with col3:
            st.markdown("### Production area for crop by Gender M/F")
            production_by_gender = village_data['Gender M/F'].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(production_by_gender, labels=production_by_gender.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
            ax2.axis('equal')
            st.pyplot(fig2)

            st.markdown("### Finished Crop by area in Acres")
            st.bar_chart(village_data['Total Area Holding (Ha)'])

        # Display table for selected village
        st.subheader(f"Farmers in {selected_village}")
        st.dataframe(village_data[['Farmer ID', 'Name of the  Farmer', 'Mobile No', 'Village', 'Total Area Holding (Ha)']])

        # Bar chart for Production by Crop in selected village
        st.subheader(f"Production by Crop in {selected_village}")
        village_production_by_crop = village_data['Production area for crop'].value_counts()
        st.bar_chart(village_production_by_crop)
    
    except KeyError as e:
        st.error(f"KeyError: {e}. Please ensure the Excel file contains the required columns.")
