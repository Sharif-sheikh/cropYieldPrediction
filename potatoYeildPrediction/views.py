from django.shortcuts import render
from .predictor import predict_crop, predict_crop_range
import pandas as pd

def about(request):
    return render(request, 'about.html')

def home(request):
    single_prediction = None
    range_predictions = []
    year = start_year = end_year = None

    if request.method == 'POST':
        if request.POST.get('prediction_type') == 'single':
            year = int(request.POST.get('year'))
            single_prediction = predict_crop(year)

        elif request.POST.get('prediction_type') == 'range':
            start_year = int(request.POST.get('start_year'))
            end_year = int(request.POST.get('end_year'))
            range_predictions = predict_crop_range(start_year, end_year)

    return render(request, 'home.html', {
        'single_prediction': single_prediction,
        'range_predictions': range_predictions,
        'year': year,
        'start_year': start_year,
        'end_year': end_year,
    })



def show_potatoes(request):
    df = pd.read_csv("FAOSTAT_data_en_5-30-2025.csv")
    potatoes_df = df[df['Item'] == 'Potatoes'].sort_values('Year')

    # Select only the columns you want
    selected_columns = ['Year', 'Value', 'Unit']
    filtered_df = potatoes_df[selected_columns]

    # Convert to HTML
    data = filtered_df.to_dict(orient='records')
    
    return render(request, 'potatoes.html', {'data': data})
