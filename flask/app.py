from flask import Flask, render_template, request, jsonify
import pandas as pd
from kafka_producer import send_to_kafka, initialize_kafka_producer

app = Flask(__name__)

# Load Parquet data
DATA_PATH = "../raw_data/neo-bank-non-sub-churn-prediction/test.parquet" 

# Load data
df = pd.read_parquet(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

# Global variable to track the latest uploaded date
latest_uploaded_date = '1999-01-01'

# Convert DataFrame to a summary grouped by date
def get_data_summary(year, month):
    filtered_df = df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]
    summary = (
        filtered_df.groupby(filtered_df['date'].dt.date)
        .size()
        .reset_index(name='count')
    )
    summary['date'] = pd.to_datetime(summary['date'])
    summary['is_uploaded'] = summary['date'].apply(lambda x: x <= pd.to_datetime(latest_uploaded_date))
    summary['date'] = summary['date'].apply(lambda x: x.strftime('%Y-%m-%d'))  # Format date here
    return summary.to_dict(orient='records')


@app.route('/')
def index():
    years = df['date'].dt.year.unique()
    year = years[0]
    month = 1
    summary = get_data_summary(year, month)
    return render_template('index.html', data=summary, years=years)

@app.route('/get_data', methods=['GET'])
def get_data():
    year = int(request.args.get('year'))
    month = int(request.args.get('month'))
    summary = get_data_summary(year, month)
    return jsonify(summary)


@app.route('/upload', methods=['POST'])
def upload_data():
    global latest_uploaded_date  # Use global variable
    if request.is_json:
        data = request.get_json()  # Get the JSON data from the request
        selected_date = data['date']  # Extract the 'date' key from the JSON
        
        # Filter data up to the selected date
        upload_df = df[df['date'] <= selected_date]
        
        # Send each row to Kafka
        for _, row in upload_df.iterrows():
            send_to_kafka(row.to_dict())  

        # Mark as uploaded and update the global variable
        latest_uploaded_date = selected_date

        return jsonify({"message": f"Data up to {selected_date} uploaded successfully!"})
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/check_kafka', methods=['GET'])
def check_kafka():
    global kafka_connected
    if initialize_kafka_producer():
        kafka_connected = True
        return jsonify({"message": "Kafka connection successful!", "status": "connected"})
    else:
        kafka_connected = False
        return jsonify({"error": "Failed to connect to Kafka", "status": "disconnected"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
