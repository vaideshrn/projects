import json
import os
from datetime import datetime

# File paths
DATA_FILE = "finances.json"

# Initialize data structure
finances = {
    "expenses": [],
    "categories": {},
    "budgets": {}
}

# Load data from file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return finances

# Save data to file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add expense
def add_expense(amount, category, description):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expense = {"timestamp": timestamp, "amount": amount, "category": category, "description": description}
    finances["expenses"].append(expense)
    save_data(finances)

# Add category
def add_category(name):
    finances["categories"][name] = 0
    save_data(finances)

# Set budget for category
def set_budget(category, budget):
    finances["budgets"][category] = budget
    save_data(finances)

# View expenses
def view_expenses():
    if not finances["expenses"]:
        print("No expenses recorded yet.")
    else:
        for expense in finances["expenses"]:
            print(f"{expense['timestamp']} - ${expense['amount']} - {expense['category']} - {expense['description']}")

# View categories
def view_categories():
    if not finances["categories"]:
        print("No categories available.")
    else:
        for category, budget in finances["categories"].items():
            print(f"{category} - Budget: ${budget}")

# Main function
def main():
    finances = load_data()
    print("Welcome to Personal Finance Manager!")
    while True:
        print("\nMenu:")
        print("1. Add Expense")
        print("2. Add Category")
        print("3. Set Budget for Category")
        print("4. View Expenses")
        print("5. View Categories")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            amount = float(input("Enter expense amount: $"))
            category = input("Enter category: ")
            description = input("Enter description: ")
            add_expense(amount, category, description)
        elif choice == "2":
            category = input("Enter category name: ")
            add_category(category)
        elif choice == "3":
            category = input("Enter category name: ")
            budget = float(input("Enter budget amount: $"))
            set_budget(category, budget)
        elif choice == "4":
            print("\nExpenses:")
            view_expenses()
        elif choice == "5":
            print("\nCategories:")
            view_categories()
        elif choice == "6":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
