import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv


load_dotenv()

# Load the data
file_path = os.getenv('DATA_PATH')
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Load the poverty data
poverty_file_path = os.getenv('POVERTY_PATH')
df_poverty = pd.read_csv(poverty_file_path, encoding='ISO-8859-1')

# Check the total number of deaths
total_deaths = len(df)
print(f"Total deaths in file: {total_deaths}")


def plot_deaths_by_month(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_cleaned = df.dropna(subset=['date'])
    df_cleaned['Year-Month'] = df_cleaned['date'].dt.to_period('M')
    monthly_deaths = df_cleaned.groupby('Year-Month').size()

    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_deaths.plot(kind='bar', ax=ax, color='skyblue', width=0.8)
    ax.set_xticklabels(monthly_deaths.index.astype(str), rotation=90)
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Number of Deaths')
    plt.title('Number of Deaths by Police (Monthly)')
    plt.tight_layout()
    plt.show()


def plot_deaths_by_month_and_race(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_cleaned = df.dropna(subset=['date'])
    df_cleaned['Year-Month'] = df_cleaned['date'].dt.to_period('M')
    monthly_deaths_by_race = df_cleaned.groupby(['Year-Month', 'race']).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_deaths_by_race.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
    ax.set_xticklabels(monthly_deaths_by_race.index.astype(str), rotation=90)
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Number of Deaths')
    plt.title('Number of Deaths by Police (Monthly, Stacked by Race)')
    plt.legend(title='Race', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_deaths_by_month_and_mental_illness(df):
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_cleaned = df.dropna(subset=['date'])
    df_cleaned['Year-Month'] = df_cleaned['date'].dt.to_period('M')
    monthly_deaths_by_mental_illness = df_cleaned.groupby(['Year-Month', 'signs_of_mental_illness']).size().unstack(
        fill_value=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_deaths_by_mental_illness.plot(kind='bar', stacked=True, ax=ax, color=['lightblue', 'orange'])
    ax.set_xticklabels(monthly_deaths_by_mental_illness.index.astype(str), rotation=90)
    ax.set_xlabel('Year-Month')
    ax.set_ylabel('Number of Deaths')
    plt.title('Number of Deaths by Police (Monthly, Stacked by Mental Illness)')
    plt.legend(title='Signs of Mental Illness', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


def plot_poverty_by_geographic_area(df_poverty):
    df_poverty['poverty_rate'] = pd.to_numeric(df_poverty['poverty_rate'], errors='coerce')
    df_poverty_cleaned = df_poverty.dropna(subset=['Geographic Area', 'poverty_rate'])
    avg_poverty_by_area = df_poverty_cleaned.groupby('Geographic Area')['poverty_rate'].mean().sort_values(
        ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    avg_poverty_by_area.plot(kind='bar', color='red', ax=ax)
    ax.set_xlabel('Geographic Area')
    ax.set_ylabel('Average Poverty Rate (%)')
    plt.title('Average Poverty Rate by Geographic Area')
    ax.set_xticklabels(avg_poverty_by_area.index, rotation=90, ha='right')
    plt.tight_layout()
    plt.show()


def plot_poverty_vs_deaths(df, df_poverty):
    df_poverty['poverty_rate'] = pd.to_numeric(df_poverty['poverty_rate'], errors='coerce')
    df_cleaned = df.dropna(subset=['state'])
    deaths_by_state = df_cleaned.groupby('state').size().reset_index(name='death_count')

    poverty_by_state = df_poverty.groupby('Geographic Area')['poverty_rate'].mean().reset_index()
    merged_data = deaths_by_state.merge(poverty_by_state, left_on='state', right_on='Geographic Area', how='left')
    merged_data.dropna(subset=['poverty_rate'], inplace=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(merged_data['poverty_rate'], merged_data['death_count'], alpha=0.7, color='blue')

    ax.set_xlabel('Poverty Rate (%)')
    ax.set_ylabel('Number of Deaths')
    ax.set_title('Scatter Plot of Deaths vs. Poverty Rate by State')

    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main_menu():
    print("\n--- Data Visualization Options ---")
    print("1: Visualize Monthly Deaths")
    print("2: Visualize Monthly Deaths by Race")
    print("3: Visualize Monthly Deaths by Mental Illness")
    print("4: Visualize Average Poverty Rate by Geographical Area")
    print("5: Compare Deaths with Poverty Rate by State")

    user_choice = input("Enter the number of the data you want to visualize: ")

    if user_choice == '1':
        plot_deaths_by_month(df)
    elif user_choice == '2':
        plot_deaths_by_month_and_race(df)
    elif user_choice == '3':
        plot_deaths_by_month_and_mental_illness(df)
    elif user_choice == '4':
        plot_poverty_by_geographic_area(df_poverty)
    elif user_choice == '5':
        plot_poverty_vs_deaths(df, df_poverty)
    else:
        print("Invalid option, please select a valid number from the menu.")
        main_menu()


main_menu()
