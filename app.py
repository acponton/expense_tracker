import sqlite3
from datetime import datetime

DB_NAME = "expense_tracker.db"


def get_connection():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    return conn


def init_db():
    """Create the expenses table if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        );
        """
    )

    conn.commit()
    conn.close()


def add_expense():
    """Prompt user for expense data and insert into the database."""
    try:
        amount_str = input("Amount: ")
        amount = float(amount_str)

        category = input("Category (e.g., Food, Rent, Transport): ").strip()
        if not category:
            print("Category cannot be empty.")
            return

        date_input = input("Date (YYYY-MM-DD, leave empty for today): ").strip()
        if date_input == "":
            date_str = datetime.now().strftime("%Y-%m-%d")
        else:
            # Basic validation: try to parse
            try:
                datetime.strptime(date_input, "%Y-%m-%d")
                date_str = date_input
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                return

        note = input("Note (optional): ").strip()

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO expenses (amount, category, date, note)
            VALUES (?, ?, ?, ?)
            """,
            (amount, category, date_str, note),
        )

        conn.commit()
        conn.close()

        print("✅ Expense added successfully.")

    except ValueError:
        print("Amount must be a number.")
    except Exception as e:
        print(f"Error adding expense: {e}")


def list_expenses():
    """List all expenses ordered by date descending."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, amount, category, date, note
        FROM expenses
        ORDER BY date DESC, id DESC
        """
    )

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No expenses found.")
        return

    print("\nID | Date       | Amount   | Category      | Note")
    print("-" * 60)
    for row in rows:
        exp_id, amount, category, date_str, note = row
        note_display = note if note else ""
        print(f"{exp_id:2} | {date_str} | ${amount:8.2f} | {category:<12} | {note_display}")
    print()


def delete_expense():
    """Show all expenses, then ask which one to delete."""
    # First show the list so the user can see IDs
    print("\nHere are your current expenses:")
    list_expenses()

    try:
        exp_id = input("Which one do you want to delete? Enter the ID: ").strip()
        if not exp_id.isdigit():
            print("ID must be a number.")
            return

        exp_id = int(exp_id)

        conn = get_connection()
        cur = conn.cursor()

        # Check if the ID exists
        cur.execute("SELECT * FROM expenses WHERE id = ?", (exp_id,))
        row = cur.fetchone()

        if not row:
            print("No expense found with that ID.")
            conn.close()
            return

        # Delete it
        cur.execute("DELETE FROM expenses WHERE id = ?", (exp_id,))
        conn.commit()
        conn.close()

        print("🗑️ Expense deleted successfully.")

    except Exception as e:
        print(f"Error deleting expense: {e}")


def report_total_spent():
    """Show the total amount spent."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT SUM(amount) FROM expenses")
    result = cur.fetchone()[0]

    conn.close()

    total = result if result is not None else 0
    print(f"\n💰 Total spent: ${total:.2f}\n")


def report_total_by_category():
    """Show total spending grouped by category."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
        ORDER BY SUM(amount) DESC
    """)

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No expenses found.")
        return

    print("\n📊 Total spent by category:")
    print("-" * 40)
    for category, total in rows:
        print(f"{category:<15}  ${total:.2f}")
    print()

def report_average_expense():
    """Show the average amount spent per expense."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT AVG(amount) FROM expenses")
    result = cur.fetchone()[0]

    conn.close()

    avg = result if result is not None else 0
    print(f"\n📈 Average expense amount: ${avg:.2f}\n")

def report_total_between_dates():
    """Show total spending between two dates."""
    start = input("Start date (YYYY-MM-DD): ").strip()
    end = input("End date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(start, "%Y-%m-%d")
        datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(amount)
        FROM expenses
        WHERE date BETWEEN ? AND ?
    """, (start, end))

    result = cur.fetchone()[0]
    conn.close()

    total = result if result is not None else 0
    print(f"\n📅 Total spent from {start} to {end}: ${total:.2f}\n")

def reports_menu():
    while True:
        print("\n=== Reports Menu ===")
        print("1. Total spent")
        print("2. Total spent by category")
        print("3. Average expense amount")
        print("4. Total spent between two dates")
        print("5. Back to main menu")

        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            report_total_spent()
        elif choice == "2":
            report_total_by_category()
        elif choice == "3":
            report_average_expense()
        elif choice == "4":
            report_total_between_dates()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

def edit_expense():
    """Edit an existing expense by ID."""
    print("\nHere are your current expenses:")
    list_expenses()

    exp_id = input("Which one do you want to edit? Enter the ID: ").strip()
    if not exp_id.isdigit():
        print("ID must be a number.")
        return

    exp_id = int(exp_id)

    conn = get_connection()
    cur = conn.cursor()

    # Fetch the existing record
    cur.execute("SELECT amount, category, date, note FROM expenses WHERE id = ?", (exp_id,))
    row = cur.fetchone()

    if not row:
        print("No expense found with that ID.")
        conn.close()
        return

    old_amount, old_category, old_date, old_note = row

    print("\nLeave any field blank to keep the current value.")
    print(f"Current amount: {old_amount}")
    new_amount = input("New amount: ").strip()

    print(f"Current category: {old_category}")
    new_category = input("New category: ").strip()

    print(f"Current date: {old_date}")
    new_date = input("New date (YYYY-MM-DD): ").strip()

    print(f"Current note: {old_note}")
    new_note = input("New note: ").strip()

    # Use old values if user leaves blank
    final_amount = float(new_amount) if new_amount else old_amount
    final_category = new_category if new_category else old_category
    final_date = new_date if new_date else old_date
    final_note = new_note if new_note else old_note

    # Validate date if changed
    if new_date:
        try:
            datetime.strptime(final_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            conn.close()
            return

    # Update the record
    cur.execute("""
        UPDATE expenses
        SET amount = ?, category = ?, date = ?, note = ?
        WHERE id = ?
    """, (final_amount, final_category, final_date, final_note, exp_id))

    conn.commit()
    conn.close()

    print(f"\n✏️ Expense updated successfully.\n")


def main_menu():
    """Simple CLI menu."""
    init_db()

    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. List all expenses")
        print("3. Delete an expense")
        print("4. Edit an expense")
        print("5. Reports")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            edit_expense()
        elif choice == "5":
            reports_menu()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    main_menu()
