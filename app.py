from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# For local file (replace 'your_dataset.xlsx' with actual path)
df = pd.read_excel('data.xlsx', engine='openpyxl')


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    transactions = df.head(15).to_dict(orient="records")
    total_txn = len(df)
    suspicious_txn = len(df[df["label"] == "Suspicious"])
    normal_txn = len(df[df["label"] == "Normal"])

    # Hour-wise transactions
    hour_data = df["hour"].value_counts().sort_index()

    hours = list(map(int, hour_data.index))
    counts = list(map(int, hour_data.values))

    return render_template(
        "dashboard.html",
        transactions=transactions,
        total_txn=total_txn,
        suspicious_txn=suspicious_txn,
        normal_txn=normal_txn,
        hours=hours,
        counts=counts
    )

if __name__ == "__main__":
    app.run(debug=True)
