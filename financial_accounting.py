"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""
from datetime import datetime
from flask import Flask
import sqlite3

app = Flask(__name__)
DATABASE = "spending.db"


def check_date(date: str) -> bool:
    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def init_db() -> None:
    conn = sqlite3.connect(DATABASE)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS expenses
    (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()


@app.route("/add/<amount>/<date>")
def add(amount: str, date: str):
    try:
        amount = float(amount)
    except ValueError:
        return "Некорректная сумма", 400

    if amount < 0:
        return "Сумма не может быть отрицательной", 400

    if not check_date(date):
        return "Некорректная дата", 400

    conn = sqlite3.connect(DATABASE)
    conn.execute("INSERT INTO expenses (date, amount) VALUES (?, ?)", (date, amount))
    conn.commit()
    conn.close()

    return f"Покупка добавлена: {date} - {amount}rub."


@app.route("/expenses")
def show_expenses():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()

    if not rows:
        return "Расходов пока нет"

    result = []
    for row in rows:
        result.append(f"{row['id']}. {row['date']}: {row['amount']}")

    return "<br>".join(result)


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row

        row = conn.execute("""
        SELECT SUM(amount) as total
        FROM expenses
        WHERE date >= ?
        AND date < ?
        """, (f"{year}-01-01", f"{year + 1}-01-01")).fetchone()

    total = row["total"]

    if total is None:
        return f"Нет расходов за {year}"

    return f"Итого за {year}: {total} rub."


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    if month < 1 or month > 12:
        return "Некорректный месяц", 400

    start = f"{year}-{month:02d}-01"

    if month == 12:
        end = f"{year + 1}-01-01"
    else:
        end = f"{year}-{month + 1:02d}-01"

    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row

        data = conn.execute("""
        SELECT SUM(amount) as total
        FROM expenses
        WHERE date >= ?
        AND date < ?
        """, (start, end)).fetchone()

    total = data['total']

    return f"Итого за {month:02d}.{year}: {total or 0} rub."


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
