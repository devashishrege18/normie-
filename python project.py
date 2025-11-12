import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import pymysql
from sqlalchemy import create_engine

print()
print()
print("################################################# WELCOME #################################################")
print("")
print("")
print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(".......")
print("....                                    TOPIC: DEATHS DUE TO CANCER                              .....")
print("........")
print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
print(" ")
print("")
print(" SCHOOL : ALPINE ACADEMY")
print(" Name : Devashish Rege")
print(" Class : XII 'PCM'    ")
print(" Roll no.:            ")
print(" Subject code : 065")
print("    ")
print(" Aim : Aim of the project is to take data stored in csv or database file and analyze using python libraries and generate appropriate charts to visualize.")
print("")
print("")
print("")

def main():
    print("=" * 100)
    print(" " * 30 + "WELCOME TO CANCER DATA ANALYSIS TOOL")
    print("=" * 100)
    print("This program analyzes cancer-related death rates across various countries and visualizes the trends.")
    print("Our aim is to provide insights into global health challenges using real-world data.")
    print("=" * 100)

    file_path = "C:\\Users\\hp\\OneDrive\\Documents\\deaths.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Error: File not found. Please check the file path and try again.")
        return

    # Clean the dataset
    columns = [
        "Country", "Country_Code", "Year", "Death_Rate", "Cancer_Type_A", "Cancer_Type_B", "Cancer_Type_C",
        "Cancer_Type_D", "Cancer_Type_E", "Cancer_Type_F", "Cancer_Type_G", "Cancer_Type_H", "Cancer_Type_I", 
        "Cancer_Type_J", "Cancer_Type_K", "Cancer_Type_L", "Cancer_Type_M", "Cancer_Type_N", "Cancer_Type_O", 
        "Cancer_Type_P", "Cancer_Type_Q", "Cancer_Type_R", "Cancer_Type_S", "Cancer_Type_T", "Cancer_Type_U", 
        "Cancer_Type_V", "Cancer_Type_W", "Cancer_Type_X", "Cancer_Type_Y", "Cancer_Type_Z", "Population_Size"
    ]
    df.columns = columns
    df_cleaned = df[["Country", "Year", "Death_Rate", "Cancer_Type_A", "Cancer_Type_B", "Population_Size"]]

    # Main menu
    while True:
        print("\n\n=== Cancer Deaths Analysis Menu ===")
        print("1. Display Data")
        print("2. Data Analysis")
        print("3. Data Visualization")
        print("4. Export Data to MySQL")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_data(df_cleaned)
        elif choice == '2':
            data_analysis(df_cleaned)
        elif choice == '3':
            data_visualization(df_cleaned)
        elif choice == '4':
            export_to_mysql(df_cleaned)
        elif choice == '5':
            print("Thank you for using the Cancer Data Analysis Tool. Stay informed!")
            break  # This will stop the loop and exit the program
        else:
            print("Invalid choice. Please try again.")

def display_data(df):
    print("\nDisplaying a sample of the dataset:")
    print("=" * 50)
    print(df.head(15))
    print("=" * 50)
    print(f"\nDataset contains {len(df)} records from {df['Country'].nunique()} countries.")
    
def export_to_mysql(df):
    try:
        # Replace NaN with None
        df = df.where(pd.notnull(df), None)

        # Create a connection to MySQL using SQLAlchemy
        engine = create_engine(
            "mysql+pymysql://root:Bisleri69@localhost/cancer_analysis"
        )

        # Export DataFrame to MySQL (automatically creates the table if it doesn't exist)
        df.to_sql(
            name="cancer_deaths",
            con=engine,
            if_exists="replace",  # Options: 'fail', 'replace', 'append'
            index=False
        )
        print("Data successfully exported to MySQL.")

    except Exception as e:
        print(f"Error exporting data to MySQL: {e}")
            
def data_analysis(df):
    print("\n\nPerforming Data Analysis...")
    print("=" * 50)

    print("Choose an analysis option:")
    print("1. Summary Statistics for Death Rate")
    print("2. Top 25 Countries with Highest Average Death Rate")
    print("3. Total Deaths by Country")
    print("4. Total Deaths for All Cancer Types")
    print("5. Year-wise Trend of Global Average Death Rate")

    choice = input("Enter your choice: ")

    if choice == '1':
        print("\nSummary Statistics for Death Rate:")
        print("=" * 50)
        print(df["Death_Rate"].describe())  # Show summary stats for Death_Rate column
        print("\nAdditional Insights:")
        print(f"Maximum Death Rate: {df['Death_Rate'].max():.2f}")
        print(f"Minimum Death Rate: {df['Death_Rate'].min():.2f}")
        print(f"Median Death Rate: {df['Death_Rate'].median():.2f}")
        print("=" * 50)

    elif choice == '2':
        print("\nTop 25 Countries with Highest Average Death Rates:")
        top_countries = df.groupby("Country")["Death_Rate"].mean().nlargest(25)
        print(top_countries)

    elif choice == '3':
        print("\nTotal Deaths by Country (All Years, All Cancer Types):")
        if 'Total_Deaths' not in df.columns:
            df = df.copy()
            df.loc[:, "Total_Deaths"] = df["Death_Rate"] * df["Population_Size"] / 100000
        total_deaths = df.groupby("Country")["Total_Deaths"].sum().sort_values(ascending=False)
        print(total_deaths)

    elif choice == '4':
        print("\nTotal Deaths for All Cancer Types Across All Countries:")
        cancer_columns = [col for col in df.columns if col.startswith("Cancer_Type")]
        total_cancer_deaths = df[cancer_columns].sum()
        print(total_cancer_deaths)

    elif choice == '5':
        print("\nYear-wise Trend of Global Average Death Rate:")
        global_avg_trend = df.groupby("Year")["Death_Rate"].mean()
        print(global_avg_trend)

    else:
        print("Invalid choice. Returning to main menu.")

    print("=" * 50)

def data_visualization(df):
    print("\nChoose a visualization type:")
    print("1. Bar Chart (Top 20 Countries by Average Death Rate)")
    print("2. Histogram (Death Rates Distribution)")
    print("3. Line Chart (Trends Over Years for All Countries)")
    print("4. Pie Chart (Proportion of Death Rates by Country)")
    print("5. Line Chart (Simple Example: Global Average Over Years)")
    print("6. Horizontal Bar Graph (Top 10 Countries by Death Rate)")

    choice = input("Enter your choice: ")

    if choice == '1':
        bar_chart(df)
    elif choice == '2':
        histogram(df)
    elif choice == '3':
        line_chart(df)
    elif choice == '4':
        pie_chart(df)
    elif choice == '5':
        simple_line_chart(df)
    elif choice == '6':
        horizontal_bar_graph(df)
    else:
        print("Invalid choice. Returning to main menu.")

def bar_chart(df):
    country_avg = df.groupby("Country")["Death_Rate"].mean().nlargest(20)
    country_avg.plot(kind='bar', color='skyblue', edgecolor='black', title='Top 20 Countries by Average Death Rate')
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.ylabel('Average Death Rate')
    plt.xlabel('Country')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def histogram(df):
    df["Death_Rate"].plot(kind='hist', bins=20, title='Distribution of Death Rates', color='orange', edgecolor='black')
    plt.xlabel('Death Rate')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

def line_chart(df):
    plt.figure(figsize=(15, 10))
    countries = df["Country"].unique()[:25]
    for country in countries:
        country_data = df[df["Country"] == country]
        plt.plot(country_data["Year"], country_data["Death_Rate"], label=country)
    plt.title('Death Rate Trends Over Years (Sample of Countries)', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Death Rate', fontsize=14)
    plt.legend(fontsize=10, loc='upper left', bbox_to_anchor=(1, 1), ncol=2)
    plt.tight_layout()
    plt.show()

def pie_chart(df):
    country_total = df.groupby("Country")["Death_Rate"].sum()
    top_countries = country_total.nlargest(5)
    top_countries.plot(kind='pie', title='Proportion of Death Rates by Top 5 Countries', autopct='%1.1f%%', startangle=90, colors=['gold', 'lightblue', 'orange', 'lightgreen', 'pink'])
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

def simple_line_chart(df):
    global_avg = df.groupby("Year")["Death_Rate"].mean()
    plt.plot(global_avg.index, global_avg.values, marker='o', linestyle='-', color='blue', label='Global Average')
    plt.title('Global Average Death Rate Over Years')
    plt.xlabel('Year')
    plt.ylabel('Average Death Rate')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def horizontal_bar_graph(df):
    avg_death_rate = df.groupby("Country")["Death_Rate"].mean().nlargest(10)
    avg_death_rate.plot(kind='barh', color='purple', edgecolor='black', title='Top 10 Countries by Average Death Rate')
    plt.xlabel('Average Death Rate')
    plt.ylabel('Country')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main() 
