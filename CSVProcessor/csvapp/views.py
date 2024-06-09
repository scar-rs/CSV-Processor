from django.shortcuts import render, redirect
from .forms import UploadCSVForm
from .models import ProcessedResults, CSVFileData
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io
import json
from django.core.exceptions import ValidationError

def get_base64_image():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close()
    return image_base64

def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_instance = form.save(commit=False)
            csv_file = csv_instance.csv_file
            df = pd.read_csv(csv_file) 
            try:
                df = df.where(pd.notnull(df), None)
                csv_data_json = df.to_json(orient='records')
                csv_instance.csv_data = json.loads(csv_data_json)
                csv_instance.save()
            except (ValueError, json.JSONDecodeError) as e:
                return render(request, 'upload_csv.html', {'form': form, 'error_message': f"Invalid JSON data: {e}"})
            except ValidationError as e:
                return render(request, 'upload_csv.html', {'form': form, 'error_message': e.message_dict})
            except Exception as e:
                return render(request, 'upload_csv.html', {'form': form, 'error_message': str(e)})
            return redirect('data_processing_options')
    else:
        form = UploadCSVForm()
    return render(request, 'upload_csv.html', {'form': form})

def data_processing_options(request):
    first_10_rows = None
    heatmap = None
    missing_data_info = None
    histograms = None
    scatter_plot_matrix = None
    violin_plot = None
    mean_median_std_results = None
    messages= []

    if request.method == 'POST':
        selected_tasks = request.POST.getlist('tasks')
        csv_instance = CSVFileData.objects.order_by('-id').first()
        if csv_instance:
            df = pd.DataFrame(csv_instance.csv_data)
        else:
            return render(request, 'data_processing_options.html', {'messages': ["No CSV file uploaded yet."]})


        if 'display_first_10_rows' in selected_tasks:
            first_10_rows = display_first_10_rows(df)

        if 'calculate_mean_median_std' in selected_tasks:
            mean_median_std_results, task_messages = calculate_mean_median_std(df)
            messages.extend(task_messages)

            for column_name, values in mean_median_std_results.items():
                processed_result = ProcessedResults(
                    column_name=column_name,
                    mean_value=values['mean'],
                    median_value=values['median'],
                    std_value=values['std']
                )
                processed_result.save()

        if 'display_heatmap' in selected_tasks:
            heatmap = generate_heatmap(df)

        if 'identify_missing_data' in selected_tasks:
            missing_data_info = identify_missing_data(df)

        if 'handle_missing_data' in selected_tasks:
            df, handle_messages = handle_missing_data(df)
            messages.extend(handle_messages)


        if 'generate_histograms' in selected_tasks:
            histograms = generate_histograms(df)

        if 'generate_scatter_plot_matrix' in selected_tasks:
            scatter_plot_matrix = generate_scatter_plot_matrix(df)

        if 'generate_violin_plot' in selected_tasks:
            violin_plot = generate_violin_plot(df)

    context = {
        'first_10_rows': first_10_rows,
        'heatmap': heatmap,
        'missing_data_info': missing_data_info,
        'histograms': histograms,
        'scatter_plot_matrix': scatter_plot_matrix,
        'violin_plot': violin_plot,
        'mean_median_std': mean_median_std_results,
        'messages':messages,
    }

    return render(request, 'data_processing_options.html', context)


def display_first_10_rows(df):
    first_10_rows = df.head(10).to_dict('records')
    return first_10_rows

def calculate_mean_median_std(df):
    results = {}
    messages = []
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            try:
                mean_value = df[column].mean()
                median_value = df[column].median()
                std_value = df[column].std()
                results[column] = {'mean': mean_value, 'median': median_value, 'std': std_value}
            except Exception as e:
                print(f"Error computing mean, median, and std for column '{column}': {e}")
        else:
            messages.append(f"Column '{column}' contains non-numeric data and cannot be processed.")
    return results,messages


def generate_heatmap(df):
    # Filter out non-numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    numeric_df = df[numeric_columns]

   
    if not numeric_df.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title('Correlation Heatmap')
        plt.xlabel('Columns')
        plt.ylabel('Columns')
        plt.tight_layout()

        # Convert the Matplotlib figure to a base64 encoded image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        return image_base64
    else:
        return None


def identify_missing_data(df):
    missing_data_info = df.isnull().sum().to_dict()
    return missing_data_info

def handle_missing_data(df):
    messages = []
    if df.isnull().sum().sum() == 0:
        messages.append("No missing values to handle.")
    else:
        for column in df.columns:
            if df[column].isnull().any():
                if pd.api.types.is_numeric_dtype(df[column]):
                    df[column].fillna(df[column].mean(), inplace=True)
                    messages.append(f"Missing values in numeric column '{column}' replaced with mean value.")
                else:
                    df[column].fillna('unknown', inplace=True)
                    messages.append(f"Missing values in string column '{column}' replaced with 'unknown'.")
    return df, messages


def generate_histograms(df):
    df.hist(figsize=(10, 8))
    plt.suptitle('Histograms for Numeric Variables', y=1.02)
    plt.tight_layout()
    return get_base64_image()

def generate_scatter_plot_matrix(df):
    sns.pairplot(df)
    plt.title('Scatter Plot Matrix')
    return get_base64_image()

def generate_violin_plot(df):
    plt.figure(figsize=(10, 8))
    sns.violinplot(data=df, inner="points")
    plt.title('Violin Plot')
    return get_base64_image()
