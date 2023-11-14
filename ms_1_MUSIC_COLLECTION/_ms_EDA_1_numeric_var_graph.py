
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_distribution(df, column):
    """
    Visualizes the distribution of a numeric column in a dataframe using a boxplot and histogram.
    
    Args:
    - df (pd.DataFrame): Input dataframe.
    - column (str): Name of the numeric column to visualize.
    """
    
    if column not in df.columns:
        print(f"Column '{column}' not found in the DataFrame.")
        return
    
    if not pd.api.types.is_numeric_dtype(df[column]):
        print(f"Column '{column}' is not numeric.")
        return

    # Set up the figure and axes
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 4]})
    
    # Boxplot
    sns.boxplot(x=df[column], ax=axes[0], color='skyblue')
    axes[0].set_title(f'Distribution of {column}')
    axes[0].xaxis.set_visible(False)  # Hide x-axis
    
    # Histogram
    sns.histplot(df[column], ax=axes[1], bins=30, kde=True)
    
    # Annotate with mean
    mean_value = df[column].mean()
    axes[1].axvline(mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')
    axes[1].legend()
    
    plt.tight_layout()
    plt.show()

# Test the function
# df = pd.read_csv('your_data_file.csv')

