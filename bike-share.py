import streamlit as st
import pandas as pd

# -----------------------------
# Constants
# -----------------------------
CITY_DATA = {
    'Chicago': 'chicago.csv',
    'New York City': 'new_york_city.csv',
    'Washington': 'washington.csv'
}
import matplotlib.pyplot as plt


def plot_user_type_pie(df):
    """
    Generates a pie chart showing the distribution of user types in the given DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        A DataFrame containing a column named 'User Type' with categorical user type data.

    Returns:
    --------
    matplotlib.figure.Figure
    """
    user_counts = df['User Type'].value_counts()
    total = user_counts.sum()
    labels = [f"{user_type}\n{count} ({count / total:.2%})" for user_type, count in user_counts.items()]
    
    fig, ax = plt.subplots()
    ax.pie(user_counts, labels=labels)
    ax.set_title('User Type Distribution')
    return fig


def plot_gender_pie(df):
    """
    Generates a pie chart showing the distribution of user genders .

    Parameters:
    -----------
    df : pandas.DataFrame
        A DataFrame containing a column named 'User Type' with categorical user type data.

    Returns:
    --------
    matplotlib.figure.Figure
    """
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        total = gender_counts.sum()
        labels = [f"{gender}\n{count} ({count / total:.2%})" for gender, count in gender_counts.items()]
        
        fig, ax = plt.subplots()
        ax.pie(gender_counts, labels=labels)
        ax.set_title('Gender Distribution')
        plt.tight_layout()
        return fig
    else:
        return None


MONTHS = ['All', 'January', 'February', 'March', 'April', 'May', 'June']
DAYS = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# -----------------------------
# Data Loading and Filtering
# -----------------------------
def load_data(city, month, day):
    """
    Loads and filters the bikeshare data based on the selected city, month, and day.

    Parameters:
    -----------
    city : str
        The name of the city to filter the data. There are three options: 'Chicago', 'New York City', and 'Washington'.
    month : str
        The month to filter the data, or 'All' for no month filter.
    day : str
        The day of the week to filter the data, or 'All' for no day filter.

    Returns:
    --------
    dataframe
    """
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        st.error(f"Data file for {city} not found.")
        return pd.DataFrame()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'All':
        df = df[df['month'] == month]
    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df

# -----------------------------
# Stats Display Functions
# -----------------------------
def show_stats(df):
    """Displays various statistics about the bikeshare data in the Streamlit app.

    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame containing the bikeshare data.
    """
    st.subheader("📊 General Stats")
    st.write(f"**Total Trips:** {len(df):,}")
    st.subheader("📅 Time Stats")
    st.write(f"**Most Common Month:** {df['month'].mode()[0]}")
    st.write(f"**Most Common Day:** {df['day_of_week'].mode()[0]}")
    st.write(f"**Most Common Start Hour:** {df['hour'].mode()[0]}")

    st.subheader("🚉 Station Stats")
    st.write(f"**Most Common Start Station:** {df['Start Station'].mode()[0]}")
    st.write(f"**Most Common End Station:** {df['End Station'].mode()[0]}")
    most_frequent_trip = (df['Start Station'] + " to " + df['End Station']).mode()[0]
    st.write(f"**Most Frequent Trip:** {most_frequent_trip}")

    st.subheader("⏱️ Trip Duration Stats")
    st.write(f"**Total Travel Time:** {df['Trip Duration'].sum():,.0f} seconds")
    st.write(f"**Average Travel Time:** {df['Trip Duration'].mean():,.2f} seconds")

    if 'Birth Year' in df.columns:
        st.subheader("🗓️ Birth Year Stats:")
        st.write(f"**Earliest:** {int(df['Birth Year'].min())}")
        st.write(f"**Most Recent:** {int(df['Birth Year'].max())}")
        st.write(f"**Most Common:** {int(df['Birth Year'].mode()[0])}")
    else:
        st.info("Birth Year data not available.")
    
    st.subheader("👥 User Type Stats")
    # Pie chart for User Type
    user_type_fig = plot_user_type_pie(df)
    st.pyplot(user_type_fig)

    st.subheader("🙋🏼‍♀️💁🏼‍♂️ Gender Stats")
    # Pie chart for Gender
    gender_fig = plot_gender_pie(df)
    if gender_fig:
        st.pyplot(gender_fig)
    else:
        st.info("Gender data not available.")

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🚲 US Bikeshare Data Explorer")

city = st.selectbox("**Select City**", list(CITY_DATA.keys()))
month = st.selectbox("**Select Month**", MONTHS)
day = st.selectbox("**Select Day**", DAYS)

if st.button("Load and Analyze Data"):
    df = load_data(city, month, day)
    if df.empty:
        st.warning("No data available for the selected filters.")
    else:
        show_stats(df)
st.subheader("📄 Raw Data Preview")
if st.checkbox("Show raw data"):
            df = load_data(city, month, day)
            num_rows = st.slider("Select number of rows to view", min_value=5, max_value=50, value=5)
            st.write(df.head(num_rows))

