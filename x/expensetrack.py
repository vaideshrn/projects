import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from tkinter.font import Font
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        
        # Load data from file
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)

        # Create custom styles
        style = ttk.Style()
        style.configure("Tab", background="lightgrey")
        style.configure("Frame.TFrame", background="lightgrey")

        self.history_frame = ttk.Frame(self.notebook, style="Frame.TFrame")
        self.notebook.add(self.history_frame, text='History')
        self.setup_history_tab()

        self.summary_frame = ttk.Frame(self.notebook, style="Frame.TFrame")
        self.notebook.add(self.summary_frame, text='Summary')
        self.setup_summary_tab()

        self.balances_frame = ttk.Frame(self.notebook, style="Frame.TFrame")
        self.notebook.add(self.balances_frame, text='Balances')
        self.setup_balances_tab()

        self.settings_frame = ttk.Frame(self.notebook, style="Frame.TFrame")
        self.notebook.add(self.settings_frame, text='Settings')
        self.setup_settings_tab()

        self.notebook.pack(expand=True, fill='both')

    def load_data(self):
        try:
            with open("expenses.json", "r") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = []

    def save_data(self):
        with open("expenses.json", "w") as f:
            json.dump(self.data, f, indent=4)

    def setup_history_tab(self):
        # Add a listbox to display transaction history
        self.history_tree = ttk.Treeview(self.history_frame, columns=("time", "account", "type", "amount", "reason"), show='tree')
        self.history_tree.pack(side="left", fill="both", expand=True)

        # Add scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_tree.config(yscrollcommand=scrollbar.set)
        
        # Populate the listbox with existing transactions
        self.update_history_tree()

        # Add "+" button to add transactions
        self.add_button = tk.Button(self.history_frame, text="+", font=("Helvetica", 20), command=self.open_add_transaction)
        self.add_button.place(relx=1.0, rely=1.0, anchor='se')  # Place button at bottom right corner
        
        # Bind right-click to delete transaction
        self.history_tree.bind("<Button-3>", self.delete_transaction)

    def update_history_tree(self):
        self.history_tree.delete(*self.history_tree.get_children())
        transactions_by_date = {}
        for entry in self.data:
            date = entry['timestamp'].split()[0]
            if date not in transactions_by_date:
                transactions_by_date[date] = []
            transactions_by_date[date].append(entry)
        
        for date, transactions in sorted(transactions_by_date.items(), reverse=True):
            parent = self.history_tree.insert("", tk.END, text=date)
            for entry in transactions:
                self.history_tree.insert(parent, tk.END, values=(entry['timestamp'].split()[1], entry['account'], entry['type'], entry['amount'], entry['reason']))

    def setup_summary_tab(self):
        # Add a dropdown menu to select previous months
        self.month_var = tk.StringVar()
        self.month_var.set(datetime.now().strftime("%B %Y"))
        self.month_dropdown = ttk.Combobox(self.summary_frame, textvariable=self.month_var)
        self.month_dropdown.pack(pady=10)
        self.month_dropdown['values'] = [datetime.now().strftime("%B %Y")]
        
        # Add a canvas for the graph
        self.graph_canvas = tk.Canvas(self.summary_frame, width=600, height=400)
        self.graph_canvas.pack(pady=10)
        
        # Show the graph
        self.show_graph()
        
    def handle_tab_change(self, event):
        if self.notebook.index("current") == 0:  # If tab 1 is selected
            self.add_button.place(relx=1.0, rely=1.0, anchor='se')  # Place button at bottom right corner
        else:
            self.add_button.place_forget()  # Hide button if other tab is selected
    
    def open_add_transaction(self):
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add Transaction")
        
        # Dropdown for account selection
        account_label = tk.Label(self.add_window, text="Account:")
        account_label.grid(row=0, column=0, padx=5, pady=5)
        self.account_var = tk.StringVar()
        self.account_dropdown = ttk.Combobox(self.add_window, textvariable=self.account_var)
        self.account_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.account_dropdown['values'] = list(set(entry['account'] for entry in self.data))  # Load existing account names
        
        # Dropdown for transaction type
        type_label = tk.Label(self.add_window, text="")
        type_label.grid(row=1, column=0, padx=5, pady=5)
        self.type_var = tk.StringVar()
        self.type_dropdown = ttk.Combobox(self.add_window, textvariable=self.type_var, values=["Expense", "Income", "Transfer"])
        self.type_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.type_dropdown.current(0)
        
        # Textbox for reason
        reason_label = tk.Label(self.add_window, text="Reason:")
        reason_label.grid(row=2, column=0, padx=5, pady=5)
        self.reason_var = tk.StringVar()
        self.reason_entry = ttk.Entry(self.add_window, textvariable=self.reason_var)
        self.reason_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Amount input
        amount_label = tk.Label(self.add_window, text="Amount:")
        amount_label.grid(row=3, column=0, padx=5, pady=5)
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(self.add_window, textvariable=self.amount_var)
        self.amount_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Keypad for amount entry
        self.keypad_frame = ttk.Frame(self.add_window)
        self.keypad_frame.grid(row=4, columnspan=2, padx=5, pady=5)
        self.create_keypad()
        
        # Time and Date input
        time_label = tk.Label(self.add_window, text="Time and Date:")
        time_label.grid(row=5, column=0, padx=5, pady=5)
        self.time_var = tk.StringVar()
        self.time_entry = ttk.Entry(self.add_window, textvariable=self.time_var)
        self.time_entry.grid(row=5, column=1, padx=5, pady=5)
        self.time_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Save button
        self.save_button = tk.Button(self.add_window, text="Save", command=self.save_transaction)
        self.save_button.grid(row=6, columnspan=2, pady=10)

    def create_keypad(self):
        buttons = [
            '7', '8', '9', '+',
            '4', '5', '6', '-',
            '1', '2', '3', '*',
            'C', '0', '=', '/'
        ]
        row, col = 0, 0
        for btn in buttons:
            ttk.Button(self.keypad_frame, text=btn, command=lambda b=btn: self.keypad_click(b)).grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def keypad_click(self, key):
        if key == "C":
            self.amount_var.set("")
        elif key == "=":
            try:
                result = str(eval(self.amount_var.get()))
                self.amount_var.set(result)
            except:
                self.amount_var.set("Error")
        else:
            current_amount = self.amount_var.get()
            if key == "0" and current_amount == "":
                return
            new_amount = current_amount + key
            self.amount_var.set(new_amount)

    def save_transaction(self):
        account = self.account_var.get()
        type_ = self.type_var.get()
        amount = float(self.amount_var.get())
        reason = self.reason_var.get()
        timestamp = self.time_var.get()

        if not all([account, type_, amount, reason, timestamp]):
            messagebox.showwarning("Warning", "All fields must be filled")
            return
        
        # Save the transaction
        self.data.append({
            "account": account,
            "type": type_,
            "amount": amount,
            "reason": reason,
            "timestamp": timestamp
        })
        
        # Save data to file
        self.save_data()

        # Update history and balances
        self.update_history_tree()
        self.update_balances()
        self.show_graph()

        self.add_window.destroy()
        messagebox.showinfo("Success", "Transaction added successfully.")

    def delete_transaction(self, event):
        selected_item = self.history_tree.selection()
        if selected_item:
            item = self.history_tree.item(selected_item)
            date = item['text']
            values = item['values']
            if values:
                time, account, type_, amount, reason = values
                timestamp = f"{date} {time}"
                confirm = messagebox.askyesno("Delete Transaction", "Are you sure you want to delete this transaction?")
                if confirm:
                    self.data = [entry for entry in self.data if entry['timestamp'] != timestamp]
                    self.save_data()
                    self.update_history_tree()
                    self.update_balances()
                    self.show_graph()
                    messagebox.showinfo("Success", "Transaction deleted successfully.")

    def show_graph(self):
        selected_date = datetime.strptime(self.month_var.get(), "%B %Y")
        start_date = selected_date.replace(day=1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(seconds=1)

        # Filter data for the selected
        filtered_data = [entry for entry in self.data if start_date <= datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S") <= end_date]

        # Create a dictionary to store daily expenses
        daily_expenses = {}
        for entry in filtered_data:
            date = datetime.strptime(entry['timestamp'], "%Y-%m-%d %H:%M:%S").day
            if entry['type'] == "Expense":
                daily_expenses[date] = daily_expenses.get(date, 0) + entry['amount']

        # Prepare data for the graph
        dates = list(daily_expenses.keys())
        amounts = list(daily_expenses.values())

        # Plot the graph
        plt.clf()
        plt.plot(dates, amounts, marker='o')
        plt.xlabel('Date')
        plt.ylabel('Amount (INR)')
        plt.title('Expenses Over Time')
        plt.xticks(range(1, 32))
        plt.yticks(range(0, int(max(amounts, default=0)) + 100, 100))
        plt.tight_layout()

        # Display the graph in the canvas
        self.graph_canvas.delete("all")
        self.graph_canvas = FigureCanvasTkAgg(plt.gcf(), master=self.graph_canvas)
        self.graph_canvas.get_tk_widget().pack(fill='both', expand=True)

    def setup_balances_tab(self):
        # Add account management frame
        self.account_frame = ttk.Frame(self.balances_frame)
        self.account_frame.pack(pady=10, fill='x')
        
        add_account_button = tk.Button(self.account_frame, text="Add Account", command=self.add_account)
        add_account_button.pack(side="left", padx=5)

        remove_account_button = tk.Button(self.account_frame, text="Remove Account", command=self.remove_account)
        remove_account_button.pack(side="left", padx=5)

        self.total_balance_label = tk.Label(self.balances_frame, text="Total Balance: 0 INR")
        self.total_balance_label.pack(pady=10)
        
        self.account_listbox = tk.Listbox(self.balances_frame, width=50, height=10)
        self.account_listbox.pack(pady=10)

        self.update_balances()

    def add_account(self):
        new_account = simpledialog.askstring("Add Account", "Enter account name:")
        if new_account:
            initial_balance = simpledialog.askfloat("Initial Balance", "Enter initial balance:", minvalue=0.0)
            self.data.append({
                "account": new_account,
                "type": "Income",
                "amount": initial_balance,
                "reason": "Initial Balance",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.save_data()
            self.update_balances()

    def remove_account(self):
        selected_account = self.account_listbox.get(tk.ACTIVE)
        if selected_account:
            account_name = selected_account.split(":")[0]
            confirm = messagebox.askyesno("Remove Account", f"Are you sure you want to remove the account '{account_name}'?")
            if confirm:
                self.data = [entry for entry in self.data if entry['account'] != account_name]
                self.save_data()
                self.update_balances()

    def update_balances(self):
        accounts = set(entry['account'] for entry in self.data)
        total_balance = 0
        self.account_listbox.delete(0, tk.END)
        for account in accounts:
            balance = sum(entry['amount'] for entry in self.data if entry['account'] == account and entry['type'] == "Income") - \
                      sum(entry['amount'] for entry in self.data if entry['account'] == account and entry['type'] == "Expense")
            self.account_listbox.insert(tk.END, f"{account}: {balance} INR")
            total_balance += balance
        self.total_balance_label.config(text=f"Total Balance: {total_balance} INR")

    def setup_settings_tab(self):
        self.settings_data = {
            "name": tk.StringVar(),
            "phone": tk.StringVar(),
            "email": tk.StringVar()
        }
        
        labels = ["Name:", "Phone Number:", "Email ID:"]
        for i, (label, key) in enumerate(zip(labels, self.settings_data.keys())):
            setting_label = tk.Label(self.settings_frame, text=label)
            setting_label.grid(row=i, column=0, padx=5, pady=5)
            setting_entry = ttk.Entry(self.settings_frame, textvariable=self.settings_data[key])
            setting_entry.grid(row=i, column=1, padx=5, pady=5)
        
        # Add a save button
        save_button = tk.Button(self.settings_frame, text="Save", command=self.save_settings)
        save_button.grid(row=len(labels), columnspan=2, pady=10)
        
        self.load_settings()

    def save_settings(self):
        settings = {key: var.get() for key, var in self.settings_data.items()}
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)
        messagebox.showinfo("Settings", "Settings saved successfully.")

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
            for key, var in self.settings_data.items():
                var.set(settings.get(key, ""))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
