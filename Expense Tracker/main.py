import datetime
import json
import matplotlib.pyplot as plt
from collections import defaultdict


def load_data():
    try:
        with open('expenses.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'expenses': []}

def save_data(data):
    with open('expenses.json', 'w') as file:
        json.dump(data, file, indent=2)
    print("Expense added successfully!")

def add_expense():
    amount = float(input("Enter the expense amount: "))
    category = input("Enter the expense category: ")
    date = input("Enter the expense date (YYYY-MM-DD, press Enter for today): ") or str(datetime.date.today())
    

    expense = {'amount': amount, 'category': category, 'date': date}
    return expense

def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\nExpense History:")
    for expense in expenses:
        print(f"Date: {expense['date']}, Category: {expense['category']}, Amount: ${expense['amount']}")

def get_unique_categories(expenses):
    return set(expense['category'] for expense in expenses)

def plot_spending_over_time(expenses, category=None):
    if not expenses:
        print("No expenses found for plotting.")
        return

    if category:
        filtered_expenses = [expense for expense in expenses if expense['category'] == category]
    else:
        filtered_expenses = expenses

    dates = defaultdict(float)
    for expense in filtered_expenses:
        dates[expense['date']] += expense['amount']

    dates = dict(dates)
    sorted_dates = sorted(dates.items(), key=lambda x: x[0])

    labels, amounts = zip(*sorted_dates)

    plt.figure(figsize=(12, 6))
    plt.plot(labels, amounts, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Total Amount Spent')
    plt.title(f'Spending Over Time ({category if category else "All Categories"})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    print("Expense Tracker")
    expenses_data = load_data()

    while True:
        print("\nOptions:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Spending Over Time")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            expense = add_expense()
            try:
                datetime.datetime.strptime(expense['date'], "%Y-%m-%d").date()
        
            except ValueError:
                print("\nInvalid date format. Please enter a valid date in YYYY-MM-DD format.")
                continue
            expenses_data['expenses'].append(expense)
            save_data(expenses_data)
            

        elif choice == '2':
            view_expenses(expenses_data['expenses'])

        elif choice == '3':
            categories = get_unique_categories(expenses_data['expenses'])
            print("Available Categories:", ", ".join(categories))
            category = input("Enter the expense category to filter (press Enter for all categories): ")
            if not category or category in categories:
                plot_spending_over_time(expenses_data['expenses'], category)
            else:
                print("Invalid Category")

        elif choice == '4':
            print("Exiting Expense Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
