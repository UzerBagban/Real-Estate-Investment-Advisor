# app.py
import streamlit as st
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns
import plotly.express as px
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Real Estate Data Analysis Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #3B82F6;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        border-left: 4px solid #3B82F6;
    }
    .info-box {
        background-color: #EFF6FF;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #60A5FA;
    }
</style>
""", unsafe_allow_html=True)

class RealEstateDashboard:
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load the cleaned data"""
        try:
            self.df = pd.read_csv('cleaned_india_housing_prices.csv')
            st.sidebar.success("✅ Data loaded successfully!")
        except FileNotFoundError:
            st.sidebar.error("❌ Data file not found. Please run data preprocessing first.")
            self.df = pd.DataFrame()
    
    def display_header(self):
        """Display the dashboard header"""
        st.markdown('<h1 class="main-header">🏠 Real Estate Data Analysis Dashboard</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #6B7280; margin-bottom: 2rem;'>
            Interactive visualization and analysis of India housing prices dataset
        </div>
        """, unsafe_allow_html=True)
    
    def display_sidebar_filters(self):
        """Display sidebar filters"""
        st.sidebar.title("🔍 Filters & Controls")
        
        if self.df.empty:
            st.sidebar.warning("No data available. Please load the dataset.")
            return
        
        # Price Range Filter
        st.sidebar.subheader("💰 Price Range")
        min_price, max_price = st.sidebar.slider(
            "Select Price Range (Lakhs)",
            min_value=float(self.df['Price_in_Lakhs'].min()),
            max_value=float(self.df['Price_in_Lakhs'].max()),
            value=(float(self.df['Price_in_Lakhs'].quantile(0.1)), 
                   float(self.df['Price_in_Lakhs'].quantile(0.9)))
        )
        
        # Size Range Filter
        st.sidebar.subheader("📏 Size Range")
        min_size, max_size = st.sidebar.slider(
            "Select Size Range (Sq Ft)",
            min_value=float(self.df['Size_in_SqFt'].min()),
            max_value=float(self.df['Size_in_SqFt'].max()),
            value=(float(self.df['Size_in_SqFt'].quantile(0.1)), 
                   float(self.df['Size_in_SqFt'].quantile(0.9)))
        )
        
        # City Filter
        st.sidebar.subheader("📍 City Filter")
        if 'City' in self.df.columns:
            cities = sorted(self.df['City'].unique())
            selected_cities = st.sidebar.multiselect(
                "Select Cities",
                options=cities,
                default=cities[:5] if len(cities) > 5 else cities
            )
        else:
            selected_cities = []
        
        # Property Type Filter
        st.sidebar.subheader("🏘️ Property Type")
        if 'Property_Type' in self.df.columns:
            property_types = sorted(self.df['Property_Type'].unique())
            selected_types = st.sidebar.multiselect(
                "Select Property Types",
                options=property_types,
                default=property_types[:3] if len(property_types) > 3 else property_types
            )
        else:
            selected_types = []
        
        # BHK Filter
        st.sidebar.subheader("🛏️ BHK Filter")
        if 'BHK' in self.df.columns:
            bhk_options = sorted(self.df['BHK'].unique())
            selected_bhk = st.sidebar.multiselect(
                "Select BHK",
                options=bhk_options,
                default=bhk_options
            )
        else:
            selected_bhk = []
        
        # Apply filters
        filtered_df = self.df.copy()
        
        # Price filter
        filtered_df = filtered_df[
            (filtered_df['Price_in_Lakhs'] >= min_price) &
            (filtered_df['Price_in_Lakhs'] <= max_price)
        ]
        
        # Size filter
        filtered_df = filtered_df[
            (filtered_df['Size_in_SqFt'] >= min_size) &
            (filtered_df['Size_in_SqFt'] <= max_size)
        ]
        
        # City filter
        if selected_cities:
            filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]
        
        # Property type filter
        if selected_types:
            filtered_df = filtered_df[filtered_df['Property_Type'].isin(selected_types)]
        
        # BHK filter
        if selected_bhk:
            filtered_df = filtered_df[filtered_df['BHK'].isin(selected_bhk)]
        
        # Display filter stats
        st.sidebar.markdown("---")
        st.sidebar.subheader("📊 Filter Stats")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.metric("Properties", len(filtered_df))
        with col2:
            st.metric("Filtered %", f"{(len(filtered_df)/len(self.df)*100):.1f}%")
        
        return filtered_df
    
    def display_key_metrics(self, filtered_df):
        """Display key metrics at the top"""
        st.markdown('<div class="sub-header">📈 Key Metrics</div>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Total Properties",
                f"{len(filtered_df):,}",
                f"{len(filtered_df)-len(self.df):+,}" if len(filtered_df) != len(self.df) else ""
            )
        
        with col2:
            avg_price = filtered_df['Price_in_Lakhs'].mean()
            st.metric(
                "Avg Price",
                f"₹{avg_price:.0f}L",
                f"₹{(avg_price - self.df['Price_in_Lakhs'].mean()):+.0f}L" if len(filtered_df) != len(self.df) else ""
            )
        
        with col3:
            avg_size = filtered_df['Size_in_SqFt'].mean()
            st.metric(
                "Avg Size",
                f"{avg_size:.0f} sq ft",
                f"{(avg_size - self.df['Size_in_SqFt'].mean()):+.0f} sq ft" if len(filtered_df) != len(self.df) else ""
            )
        
        with col4:
            avg_pps = filtered_df['Price_per_SqFt'].mean()
            st.metric(
                "Avg Price/Sq Ft",
                f"₹{avg_pps:.0f}",
                f"₹{(avg_pps - self.df['Price_per_SqFt'].mean()):+.0f}" if len(filtered_df) != len(self.df) else ""
            )
        
        with col5:
            if 'BHK' in filtered_df.columns:
                common_bhk = filtered_df['BHK'].mode()[0] if not filtered_df['BHK'].mode().empty else "N/A"
                st.metric(
                    "Most Common BHK",
                    f"{common_bhk}"
                )
    
    def display_price_analysis(self, filtered_df):
        """Display price analysis visualizations"""
        st.markdown('<div class="sub-header">💰 Price Analysis</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution", "📈 Trends", "🏙️ By City", "🏘️ By Type"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Price Distribution Histogram
                fig1 = px.histogram(
                    filtered_df,
                    x='Price_in_Lakhs',
                    nbins=50,
                    title='Property Price Distribution',
                    labels={'Price_in_Lakhs': 'Price (Lakhs)'},
                    color_discrete_sequence=['#3B82F6']
                )
                fig1.add_vline(
                    x=filtered_df['Price_in_Lakhs'].median(),
                    line_dash="dash",
                    line_color="red",
                    annotation_text=f"Median: ₹{filtered_df['Price_in_Lakhs'].median():.0f}L"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Price per Sq Ft Distribution
                fig2 = px.box(
                    filtered_df,
                    y='Price_per_SqFt',
                    title='Price per Sq Ft Distribution',
                    labels={'Price_per_SqFt': 'Price per Sq Ft'}
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Size vs Price Scatter
                fig3 = px.scatter(
                    filtered_df,
                    x='Size_in_SqFt',
                    y='Price_in_Lakhs',
                    color='Price_per_SqFt',
                    size='Price_in_Lakhs',
                    hover_data=['City', 'Property_Type', 'BHK'] if 'City' in filtered_df.columns else None,
                    title='Property Size vs Price',
                    labels={
                        'Size_in_SqFt': 'Size (Sq Ft)',
                        'Price_in_Lakhs': 'Price (Lakhs)',
                        'Price_per_SqFt': 'Price/Sq Ft'
                    },
                    color_continuous_scale='viridis'
                )
                st.plotly_chart(fig3, use_container_width=True)
            
            with col2:
                # Price vs BHK
                if 'BHK' in filtered_df.columns:
                    fig4 = px.box(
                        filtered_df,
                        x='BHK',
                        y='Price_in_Lakhs',
                        title='Price Distribution by BHK',
                        labels={'Price_in_Lakhs': 'Price (Lakhs)'}
                    )
                    st.plotly_chart(fig4, use_container_width=True)
        
        with tab3:
            if 'City' in filtered_df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Top Cities by Average Price
                    city_avg_price = filtered_df.groupby('City')['Price_in_Lakhs'].mean().sort_values(ascending=False).head(10)
                    
                    fig5 = px.bar(
                        x=city_avg_price.values,
                        y=city_avg_price.index,
                        orientation='h',
                        title='Top 10 Cities by Average Price',
                        labels={'x': 'Average Price (Lakhs)', 'y': 'City'},
                        color=city_avg_price.values,
                        color_continuous_scale='Blues'
                    )
                    st.plotly_chart(fig5, use_container_width=True)
                
                with col2:
                    # Price Distribution by City
                    top_cities = filtered_df['City'].value_counts().head(5).index
                    top_cities_data = filtered_df[filtered_df['City'].isin(top_cities)]
                    
                    fig6 = px.box(
                        top_cities_data,
                        x='City',
                        y='Price_in_Lakhs',
                        title='Price Distribution in Top 5 Cities',
                        labels={'Price_in_Lakhs': 'Price (Lakhs)'}
                    )
                    st.plotly_chart(fig6, use_container_width=True)
        
        with tab4:
            if 'Property_Type' in filtered_df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Average Price by Property Type
                    type_avg_price = filtered_df.groupby('Property_Type')['Price_in_Lakhs'].mean().sort_values(ascending=False)
                    
                    fig7 = px.bar(
                        x=type_avg_price.values,
                        y=type_avg_price.index,
                        orientation='h',
                        title='Average Price by Property Type',
                        labels={'x': 'Average Price (Lakhs)', 'y': 'Property Type'},
                        color=type_avg_price.values,
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig7, use_container_width=True)
                
                with col2:
                    # Price per Sq Ft by Property Type
                    fig8 = px.box(
                        filtered_df,
                        x='Property_Type',
                        y='Price_per_SqFt',
                        title='Price per Sq Ft by Property Type',
                        labels={'Price_per_SqFt': 'Price per Sq Ft'}
                    )
                    fig8.update_xaxes(tickangle=45)
                    st.plotly_chart(fig8, use_container_width=True)
    
    def display_location_analysis(self, filtered_df):
        """Display location-based analysis"""
        st.markdown('<div class="sub-header">📍 Location Analysis</div>', unsafe_allow_html=True)
        
        if 'City' not in filtered_df.columns:
            st.warning("City data not available for location analysis.")
            return
        
        tab1, tab2, tab3 = st.tabs(["🏙️ City Overview", "📊 City Comparison", "🗺️ Geographical View"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # City-wise property count
                city_counts = filtered_df['City'].value_counts().head(15)
                
                fig1 = px.bar(
                    x=city_counts.values,
                    y=city_counts.index,
                    orientation='h',
                    title='Top 15 Cities by Property Count',
                    labels={'x': 'Number of Properties', 'y': 'City'},
                    color=city_counts.values,
                    color_continuous_scale='Purples'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # City statistics table
                city_stats = filtered_df.groupby('City').agg({
                    'Price_in_Lakhs': ['mean', 'median', 'count'],
                    'Size_in_SqFt': 'mean',
                    'Price_per_SqFt': 'mean'
                }).round(2)
                
                city_stats.columns = ['Avg Price', 'Median Price', 'Count', 'Avg Size', 'Avg Price/Sq Ft']
                city_stats = city_stats.sort_values('Avg Price', ascending=False).head(10)
                
                st.dataframe(city_stats, use_container_width=True)
        
        with tab2:
            # Interactive city comparison
            st.subheader("Compare Cities")
            
            if 'City' in filtered_df.columns:
                cities = filtered_df['City'].unique()
                selected_cities = st.multiselect(
                    "Select cities to compare:",
                    options=cities,
                    default=cities[:3] if len(cities) >= 3 else cities
                )
                
                if selected_cities:
                    comparison_data = filtered_df[filtered_df['City'].isin(selected_cities)]
                    
                    # Create comparison charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig2 = px.box(
                            comparison_data,
                            x='City',
                            y='Price_in_Lakhs',
                            title='Price Comparison',
                            labels={'Price_in_Lakhs': 'Price (Lakhs)'}
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    with col2:
                        fig3 = px.box(
                            comparison_data,
                            x='City',
                            y='Size_in_SqFt',
                            title='Size Comparison',
                            labels={'Size_in_SqFt': 'Size (Sq Ft)'}
                        )
                        st.plotly_chart(fig3, use_container_width=True)
                    
                    # Additional metrics
                    st.subheader("City Metrics Comparison")
                    metrics_df = comparison_data.groupby('City').agg({
                        'Price_in_Lakhs': ['mean', 'median', 'std'],
                        'Size_in_SqFt': ['mean', 'median'],
                        'Price_per_SqFt': 'mean',
                        'BHK': 'mean'
                    }).round(2)
                    
                    metrics_df.columns = ['Avg Price', 'Median Price', 'Price Std', 
                                         'Avg Size', 'Median Size', 'Avg Price/Sq Ft', 'Avg BHK']
                    
                    st.dataframe(metrics_df, use_container_width=True)
        
        with tab3:
            # Simple geographical representation (if coordinates available)
            st.info("For geographical visualization, latitude/longitude data would be needed.")
            
            # Alternative: Sunburst chart for hierarchical location data
            if all(col in filtered_df.columns for col in ['State', 'City', 'Locality']):
                # Sample data for sunburst
                location_hierarchy = filtered_df.groupby(['State', 'City', 'Locality']).size().reset_index(name='Count')
                
                fig4 = px.sunburst(
                    location_hierarchy.head(100),  # Limit for performance
                    path=['State', 'City', 'Locality'],
                    values='Count',
                    title='Property Distribution Hierarchy',
                    color='Count',
                    color_continuous_scale='RdBu'
                )
                st.plotly_chart(fig4, use_container_width=True)
    
    def display_property_features_analysis(self, filtered_df):
        """Display analysis of property features"""
        st.markdown('<div class="sub-header">🏘️ Property Features Analysis</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["🛏️ BHK Analysis", "🛋️ Furnishing", "🚗 Parking", "🎯 Amenities"])
        
        with tab1:
            if 'BHK' in filtered_df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    # BHK Distribution
                    bhk_dist = filtered_df['BHK'].value_counts().sort_index()
                    
                    fig1 = px.pie(
                        values=bhk_dist.values,
                        names=bhk_dist.index,
                        title='BHK Distribution',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Blues
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    # Price by BHK
                    bhk_price = filtered_df.groupby('BHK')['Price_in_Lakhs'].agg(['mean', 'median', 'std']).reset_index()
                    
                    fig2 = px.bar(
                        bhk_price,
                        x='BHK',
                        y='mean',
                        error_y='std',
                        title='Average Price by BHK',
                        labels={'mean': 'Average Price (Lakhs)', 'BHK': 'Number of Bedrooms'},
                        color='mean',
                        color_continuous_scale='Greens'
                    )
                    st.plotly_chart(fig2, use_container_width=True)
        
        with tab2:
            if 'Furnished_Status' in filtered_df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Furnishing Status Distribution
                    furnish_dist = filtered_df['Furnished_Status'].value_counts()
                    
                    fig3 = px.bar(
                        x=furnish_dist.values,
                        y=furnish_dist.index,
                        orientation='h',
                        title='Furnishing Status Distribution',
                        labels={'x': 'Count', 'y': 'Furnishing Status'},
                        color=furnish_dist.values,
                        color_continuous_scale='Oranges'
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                
                with col2:
                    # Price by Furnishing Status
                    furnish_price = filtered_df.groupby('Furnished_Status')['Price_per_SqFt'].agg(['mean', 'std', 'count']).reset_index()
                    
                    fig4 = px.bar(
                        furnish_price,
                        x='Furnished_Status',
                        y='mean',
                        error_y='std',
                        title='Price per Sq Ft by Furnishing Status',
                        labels={'mean': 'Average Price per Sq Ft'},
                        color='mean',
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig4, use_container_width=True)
        
        with tab3:
            if 'Parking_Space' in filtered_df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Parking Space Distribution
                    parking_dist = filtered_df['Parking_Space'].value_counts().sort_index()
                    
                    fig5 = px.bar(
                        x=parking_dist.index,
                        y=parking_dist.values,
                        title='Parking Space Distribution',
                        labels={'x': 'Parking Spaces', 'y': 'Count'},
                        color=parking_dist.values,
                        color_continuous_scale='Purples'
                    )
                    st.plotly_chart(fig5, use_container_width=True)
                
                with col2:
                    # Price vs Parking
                    parking_price = filtered_df.groupby('Parking_Space')['Price_in_Lakhs'].mean().reset_index()
                    
                    fig6 = px.line(
                        parking_price,
                        x='Parking_Space',
                        y='Price_in_Lakhs',
                        title='Average Price by Parking Spaces',
                        labels={'Price_in_Lakhs': 'Average Price (Lakhs)'},
                        markers=True
                    )
                    fig6.update_traces(line=dict(color='blue', width=3))
                    st.plotly_chart(fig6, use_container_width=True)
        
        with tab4:
            if 'Amenities' in filtered_df.columns:
                # Analyze common amenities
                st.subheader("Amenities Analysis")
                
                # Common amenities to check
                common_amenities = ['Gym', 'Pool', 'Clubhouse', 'Garden', 'Park', 'Security', 'Lift', 'Power Backup']
                
                amenity_analysis = []
                for amenity in common_amenities:
                    has_amenity = filtered_df['Amenities'].str.contains(amenity, case=False, na=False)
                    if has_amenity.any():
                        count_with = has_amenity.sum()
                        percentage = (count_with / len(filtered_df)) * 100
                        avg_price_with = filtered_df[has_amenity]['Price_per_SqFt'].mean()
                        avg_price_without = filtered_df[~has_amenity]['Price_per_SqFt'].mean()
                        price_premium = ((avg_price_with / avg_price_without) - 1) * 100 if avg_price_without > 0 else 0
                        
                        amenity_analysis.append({
                            'Amenity': amenity,
                            'Count': count_with,
                            'Percentage': percentage,
                            'Avg Price/Sq Ft (With)': avg_price_with,
                            'Avg Price/Sq Ft (Without)': avg_price_without,
                            'Price Premium %': price_premium
                        })
                
                if amenity_analysis:
                    amenity_df = pd.DataFrame(amenity_analysis)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Amenity popularity
                        fig7 = px.bar(
                            amenity_df.sort_values('Percentage', ascending=True),
                            x='Percentage',
                            y='Amenity',
                            orientation='h',
                            title='Amenity Popularity (%)',
                            color='Percentage',
                            color_continuous_scale='Blues'
                        )
                        st.plotly_chart(fig7, use_container_width=True)
                    
                    with col2:
                        # Price premium
                        fig8 = px.bar(
                            amenity_df.sort_values('Price Premium %', ascending=True),
                            x='Price Premium %',
                            y='Amenity',
                            orientation='h',
                            title='Price Premium for Amenities (%)',
                            color='Price Premium %',
                            color_continuous_scale='RdYlGn'
                        )
                        st.plotly_chart(fig8, use_container_width=True)
                    
                    # Display table
                    st.subheader("Detailed Amenities Analysis")
                    st.dataframe(amenity_df.round(2), use_container_width=True)
    
    def display_correlation_analysis(self, filtered_df):
        """Display correlation analysis"""
        st.markdown('<div class="sub-header">🔗 Correlation Analysis</div>', unsafe_allow_html=True)
        
        # Select numerical columns for correlation
        numerical_cols = filtered_df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) < 2:
            st.warning("Not enough numerical columns for correlation analysis.")
            return
        
        # Correlation matrix
        corr_matrix = filtered_df[numerical_cols].corr()
        
        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect='auto',
            color_continuous_scale='RdBu_r',
            title='Correlation Matrix Heatmap',
            labels=dict(color='Correlation')
        )
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top correlations
        st.subheader("Top Correlations")
        
        # Flatten correlation matrix
        corr_pairs = corr_matrix.unstack().sort_values(ascending=False)
        
        # Get top positive correlations (excluding self-correlations)
        top_pos = corr_pairs[corr_pairs < 1].head(5)
        
        # Get top negative correlations
        top_neg = corr_pairs.tail(5)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top Positive Correlations:**")
            for (var1, var2), corr in top_pos.items():
                st.write(f"• {var1} ↔ {var2}: **{corr:.3f}**")
        
        with col2:
            st.write("**Top Negative Correlations:**")
            for (var1, var2), corr in top_neg.items():
                st.write(f"• {var1} ↔ {var2}: **{corr:.3f}**")
        
        # Price correlation insights
        if 'Price_in_Lakhs' in numerical_cols:
            st.subheader("Price Correlation Insights")
            
            price_correlations = corr_matrix['Price_in_Lakhs'].sort_values(ascending=False)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Strongest Positive",
                    f"{price_correlations.index[1] if len(price_correlations) > 1 else 'N/A'}",
                    f"{price_correlations.iloc[1]:.3f}"
                )
            
            with col2:
                st.metric(
                    "Strongest Negative",
                    f"{price_correlations.index[-1] if len(price_correlations) > 0 else 'N/A'}",
                    f"{price_correlations.iloc[-1]:.3f}"
                )
            
            with col3:
                size_corr = filtered_df['Size_in_SqFt'].corr(filtered_df['Price_in_Lakhs'])
                st.metric(
                    "Size-Price Correlation",
                    f"{size_corr:.3f}",
                    "Strong" if abs(size_corr) > 0.7 else "Moderate" if abs(size_corr) > 0.3 else "Weak"
                )
    
    def display_data_explorer(self, filtered_df):
        """Display interactive data explorer"""
        st.markdown('<div class="sub-header">🔍 Data Explorer</div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["📋 Raw Data", "📊 Summary", "📈 Custom Charts"])
        
        with tab1:
            # Data preview
            st.subheader("Filtered Data Preview")
            
            # Number of rows to show
            rows_to_show = st.slider("Number of rows to display", 10, 500, 100)
            
            # Column selector
            all_columns = filtered_df.columns.tolist()
            selected_columns = st.multiselect(
                "Select columns to display:",
                options=all_columns,
                default=all_columns[:10]  # Show first 10 columns by default
            )
            
            if selected_columns:
                st.dataframe(
                    filtered_df[selected_columns].head(rows_to_show),
                    use_container_width=True,
                    height=400
                )
                
                # Download button
                csv = filtered_df[selected_columns].to_csv(index=False)
                st.download_button(
                    label="📥 Download Filtered Data (CSV)",
                    data=csv,
                    file_name="filtered_real_estate_data.csv",
                    mime="text/csv"
                )
        
        with tab2:
            # Data summary
            st.subheader("Data Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Basic statistics
                st.write("**Basic Statistics:**")
                st.dataframe(filtered_df.describe(), use_container_width=True)
            
            with col2:
                # Column information
                st.write("**Column Information:**")
                
                column_info = pd.DataFrame({
                    'Column': filtered_df.columns,
                    'Data Type': filtered_df.dtypes.values,
                    'Non-Null Count': filtered_df.count().values,
                    'Null Count': filtered_df.isnull().sum().values,
                    'Unique Values': [filtered_df[col].nunique() for col in filtered_df.columns]
                })
                
                st.dataframe(column_info, use_container_width=True, height=400)
        
        with tab3:
            # Custom chart builder
            st.subheader("Custom Chart Builder")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # X-axis selector
                x_axis = st.selectbox(
                    "Select X-axis variable:",
                    options=filtered_df.columns.tolist(),
                    index=0
                )
            
            with col2:
                # Y-axis selector
                y_axis = st.selectbox(
                    "Select Y-axis variable:",
                    options=filtered_df.select_dtypes(include=[np.number]).columns.tolist(),
                    index=1 if len(filtered_df.select_dtypes(include=[np.number]).columns) > 1 else 0
                )
            
            with col3:
                # Chart type selector
                chart_type = st.selectbox(
                    "Select chart type:",
                    options=['Scatter', 'Line', 'Bar', 'Histogram', 'Box', 'Violin']
                )
            
            # Color selector
            color_by = st.selectbox(
                "Color by (optional):",
                options=['None'] + filtered_df.columns.tolist()
            )
            
            # Create chart based on selections
            if x_axis and y_axis:
                if chart_type == 'Scatter':
                    fig = px.scatter(
                        filtered_df,
                        x=x_axis,
                        y=y_axis,
                        color=None if color_by == 'None' else color_by,
                        title=f'{y_axis} vs {x_axis}',
                        hover_data=filtered_df.columns.tolist()[:5]
                    )
                
                elif chart_type == 'Line':
                    # For line charts, we need to aggregate if x is categorical
                    if filtered_df[x_axis].dtype == 'object':
                        agg_data = filtered_df.groupby(x_axis)[y_axis].mean().reset_index()
                        fig = px.line(
                            agg_data,
                            x=x_axis,
                            y=y_axis,
                            title=f'{y_axis} by {x_axis}',
                            markers=True
                        )
                    else:
                        fig = px.line(
                            filtered_df.sort_values(x_axis),
                            x=x_axis,
                            y=y_axis,
                            title=f'{y_axis} vs {x_axis}'
                        )
                
                elif chart_type == 'Bar':
                    # For bar charts, aggregate categorical x
                    if filtered_df[x_axis].dtype == 'object':
                        agg_data = filtered_df.groupby(x_axis)[y_axis].mean().reset_index()
                        fig = px.bar(
                            agg_data,
                            x=x_axis,
                            y=y_axis,
                            title=f'Average {y_axis} by {x_axis}',
                            color=None if color_by == 'None' else color_by
                        )
                    else:
                        # If x is numerical, create histogram-like bar
                        fig = px.histogram(
                            filtered_df,
                            x=x_axis,
                            y=y_axis,
                            title=f'{y_axis} distribution by {x_axis}',
                            histfunc='avg'
                        )
                
                elif chart_type == 'Histogram':
                    fig = px.histogram(
                        filtered_df,
                        x=y_axis,
                        title=f'Distribution of {y_axis}',
                        color=None if color_by == 'None' else color_by,
                        nbins=50
                    )
                
                elif chart_type == 'Box':
                    fig = px.box(
                        filtered_df,
                        x=x_axis,
                        y=y_axis,
                        title=f'{y_axis} by {x_axis}',
                        color=None if color_by == 'None' else color_by
                    )
                
                elif chart_type == 'Violin':
                    fig = px.violin(
                        filtered_df,
                        x=x_axis,
                        y=y_axis,
                        title=f'{y_axis} distribution by {x_axis}',
                        color=None if color_by == 'None' else color_by,
                        box=True
                    )
                
                # Display the chart
                if 'fig' in locals():
                    st.plotly_chart(fig, use_container_width=True)
    
    def display_insights_summary(self, filtered_df):
        """Display insights and summary"""
        st.markdown('<div class="sub-header">💡 Key Insights</div>', unsafe_allow_html=True)
        
        # Create insights based on the filtered data
        insights = []
        
        # Insight 1: Price distribution
        price_skew = filtered_df['Price_in_Lakhs'].skew()
        if abs(price_skew) > 1:
            insights.append(f"📊 **Price Distribution**: Prices are {'right' if price_skew > 0 else 'left'} skewed (skewness: {price_skew:.2f}), indicating {'few high-value properties' if price_skew > 0 else 'concentration in lower price range'}.")
        
        # Insight 2: Size-Price relationship
        size_price_corr = filtered_df['Size_in_SqFt'].corr(filtered_df['Price_in_Lakhs'])
        if size_price_corr > 0.5:
            insights.append(f"📏 **Size-Price Relationship**: Strong positive correlation ({size_price_corr:.2f}) between property size and price.")
        elif size_price_corr < 0:
            insights.append(f"📏 **Size-Price Relationship**: Negative correlation ({size_price_corr:.2f}) - larger properties may not always command higher prices.")
        
        # Insight 3: City insights
        if 'City' in filtered_df.columns:
            top_city = filtered_df.groupby('City')['Price_in_Lakhs'].mean().idxmax()
            top_city_price = filtered_df.groupby('City')['Price_in_Lakhs'].mean().max()
            insights.append(f"🏙️ **Most Expensive City**: {top_city} has the highest average price (₹{top_city_price:.0f}L).")
        
        # Insight 4: BHK insights
        if 'BHK' in filtered_df.columns:
            common_bhk = filtered_df['BHK'].mode()[0] if not filtered_df['BHK'].mode().empty else 'N/A'
            insights.append(f"🛏️ **Popular Configuration**: {common_bhk} BHK is the most common configuration.")
        
        # Insight 5: Price per Sq Ft range
        pps_min = filtered_df['Price_per_SqFt'].min()
        pps_max = filtered_df['Price_per_SqFt'].max()
        pps_avg = filtered_df['Price_per_SqFt'].mean()
        insights.append(f"💰 **Price Range**: Price per sq ft ranges from ₹{pps_min:.0f} to ₹{pps_max:.0f}, with an average of ₹{pps_avg:.0f}.")
        
        # Display insights
        for i, insight in enumerate(insights, 1):
            st.markdown(f"""
            <div class="info-box">
                <strong>Insight #{i}:</strong> {insight}
            </div>
            """, unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("""
        <div class="info-box">
            <strong>🎯 Recommendations for Further Analysis:</strong>
            <ul>
                <li>Consider time-series analysis if year/month data is available</li>
                <li>Analyze seasonal trends in property prices</li>
                <li>Compare price trends across different property types</li>
                <li>Investigate the impact of specific amenities on prices</li>
                <li>Analyze price trends in developing vs established areas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Main method to run the dashboard"""
        self.display_header()
        
        if self.df.empty:
            st.error("""
            ## ❌ Data Not Found
            
            Please ensure:
            1. You have run the data preprocessing script
            2. The file `cleaned_india_housing_prices.csv` exists in the same directory
            3. You have the necessary permissions to read the file
            
            To preprocess the data, run:
            ```python
            # Save the data preprocessing code in a file
            python data_preprocessing.py
            ```
            """)
            return
        
        # Display filters and get filtered data
        filtered_df = self.display_sidebar_filters()
        
        # Display all sections
        self.display_key_metrics(filtered_df)
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "💰 Price Analysis", 
            "📍 Location Analysis", 
            "🏘️ Features", 
            "🔗 Correlations", 
            "🔍 Data Explorer", 
            "💡 Insights"
        ])
        
        with tab1:
            self.display_price_analysis(filtered_df)
        
        with tab2:
            self.display_location_analysis(filtered_df)
        
        with tab3:
            self.display_property_features_analysis(filtered_df)
        
        with tab4:
            self.display_correlation_analysis(filtered_df)
        
        with tab5:
            self.display_data_explorer(filtered_df)
        
        with tab6:
            self.display_insights_summary(filtered_df)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #6B7280; padding: 1rem;'>
            <p>📊 Real Estate Data Analysis Dashboard | Built with Streamlit</p>
            <p>Dataset: India Housing Prices | Properties: {:,} | Last Updated: {}</p>
        </div>
        """.format(len(self.df), pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')), unsafe_allow_html=True)

# Run the dashboard
if __name__ == "__main__":
    dashboard = RealEstateDashboard()
    dashboard.run()