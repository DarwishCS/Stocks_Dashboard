from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_finviz_data():
    url = "https://finviz.com/screener.ashx?v=111&o=-volume"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    stocks = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"class": "screener_table"})
        rows = table.find_all("tr")[1:]  # Skip the header row

        for row in rows:
            columns = row.find_all("td")
            if len(columns) > 1:
                ticker = columns[1].text.strip()
                name = columns[2].text.strip()
                price = columns[8].text.strip()
                volume = columns[5].text.strip()
                stocks.append({"Ticker": ticker, "Name": name, "Price": price, "Volume": volume})

    return stocks

@app.route("/")
def home():
    stocks = get_finviz_data()
    # Render the data in an HTML table
    return render_template_string('''
        <h1>Finviz Stock Screener</h1>
        <table border="1">
            <tr>
                <th>Ticker</th>
                <th>Name</th>
                <th>Price</th>
                <th>Volume</th>
            </tr>
            {% for stock in stocks %}
            <tr>
                <td>{{ stock.Ticker }}</td>
                <td>{{ stock.Name }}</td>
                <td>{{ stock.Price }}</td>
                <td>{{ stock.Volume }}</td>
            </tr>
            {% endfor %}
        </table>
    ''', stocks=stocks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)