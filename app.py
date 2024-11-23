# Install required packages before running: pip install streamlit pandas geopandas folium streamlit-folium plotly geopy

import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Load population data (CSV)
population_data = pd.read_csv('data/world_population.csv')

# Clean column names by stripping whitespace and removing unwanted characters
population_data.columns = population_data.columns.str.strip()
population_data.columns = population_data.columns.str.replace('Â', '', regex=False)

# Load geospatial data (GeoJSON)
world = gpd.read_file('data/world.geojson')

# Title and Description
st.title("🌍 World Population Dashboard")
st.markdown("""
Explore population data and trends for countries worldwide with interactive visualizations and maps. 
Select a country to see detailed insights, historical trends, and geospatial data.
""")

# Country selection dropdown with India as the default option
st.sidebar.header("🔍 Select a Country")
country_options = population_data['Country/Territory'].unique()

# Set India as the default country
selected_country = st.sidebar.selectbox('Choose a Country', country_options, index=list(country_options).index('India'))

# Filter the data for the selected country
country_data = population_data[population_data['Country/Territory'] == selected_country].iloc[0]

# Display key information about the selected country
st.subheader(f"Country: **{selected_country}**")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Capital**: {country_data['Capital']}")
    st.write(f"**Continent**: {country_data['Continent']}")
    st.write(f"**Area**: {country_data['Area (km²)']} km²")
with col2:
    st.write(f"**Density**: {country_data['Density (per km²)']} people/km²")
    st.write(f"**Growth Rate**: {country_data['Growth Rate']}%")
    st.write(f"**World Population Percentage**: {country_data['World Population Percentage']}%")

# Population trend visualization
st.subheader("📊 Population Trends Over Time")
years = ['1970 Population', '1980 Population', '1990 Population', '2000 Population', 
         '2010 Population', '2020 Population', '2022 Population']
population_trend = {year: country_data[year] for year in years}
trend_df = pd.DataFrame(list(population_trend.items()), columns=["Year", "Population"])
fig = px.line(trend_df, x="Year", y="Population", markers=True, 
              title=f"Population Trends for {selected_country}")
st.plotly_chart(fig, use_container_width=True)

# Map visualization
st.subheader("🗺️ Country Map with Capital Location")
geodata = world[world['name'] == selected_country]
if not geodata.empty:
    # Get the centroid for mapping
    country_geometry = geodata.geometry.iloc[0]
    centroid = country_geometry.centroid
    capital_lat = centroid.y
    capital_lon = centroid.x

    # Create a map, centering on India's capital by default
    m = folium.Map(location=[capital_lat, capital_lon], zoom_start=5)
    folium.Marker(location=[capital_lat, capital_lon], 
                  popup=f"Capital: {country_data['Capital']}").add_to(m)
    folium.GeoJson(country_geometry, name="Country Boundary").add_to(m)
    st_folium(m, width=800, height=400)
else:
    st.write("Map data for this country is not available.")

# Add a footer with your name and social links
st.markdown("""
---
👨‍💻 Developed by [Manjar Alam](https://www.linkedin.com/in/manjar-alam-4a42b3206/)  
🔗 [GitHub](https://github.com/Manjar-Alam)
""")
