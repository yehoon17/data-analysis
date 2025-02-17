from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Load Parquet data
DATA_PATH = "../raw_data/neo-bank-non-sub-churn-prediction/test.parquet" # TODO: integrate docker compose via volume 
UPLOAD_LOG = "uploaded_log.json"

# Load data
df = pd.read_parquet(DATA_PATH)
df['date'] = pd.to_datetime(df['date'])

# Load upload tracking log
try:
    with open(UPLOAD_LOG, "r") as f:
        uploaded_log = json.load(f)
except FileNotFoundError:
    uploaded_log = {}

# Convert DataFrame to a summary grouped by date
def get_data_summary(year, month):
    filtered_df = df[(df['date'].dt.year == year) & (df['date'].dt.month == month)]
    summary = (
        filtered_df.groupby(filtered_df['date'].dt.date)
        .size()
        .reset_index(name='count')
    )
    summary['date'] = summary['date'].apply(lambda x: x.strftime('%Y-%m-%d'))  # Format date here
    summary['is_uploaded'] = summary['date'].astype(str).map(uploaded_log).fillna(False)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
