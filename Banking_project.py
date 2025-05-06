import json
import os
from datetime import date

class BankAccount:
    # Initialize the BankAccount class
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.transactions = []

    # Deposit function
    def deposit(self, amount):
        try:
            if amount > 0:
                self.balance += amount
                self.record_transaction("Deposit", amount)
                print(f"Deposited ${amount} into account {self.account_number}. New Balance: ${self.balance}")
            else:
                print("Deposit amount must be positive.")
        except Exception as e:
            print(f"Error during deposit: {e}")

    # Withdraw function
    def withdraw(self, amount):
        try:
            if 0 < amount <= self.balance:
                self.balance -= amount
                self.record_transaction("Withdrawal", amount)
                print(f"Withdrew ${amount} from account {self.account_number}. New Balance: ${self.balance}")
            else:
                print("Insufficient balance or invalid amount.")
        except Exception as e:
            print(f"Error during withdrawal: {e}")

    # Transfer function
    def transfer(self, target_account, amount):
        try:
            if 0 < amount <= self.balance:
                self.withdraw(amount)
                target_account.deposit(amount)
                print(f"Transferred ${amount} to account {target_account.account_number}.")
            else:
                print("Insufficient balance or invalid amount.")
        except Exception as e:
            print(f"Error during transfer: {e}")

    # Record a transaction
    def record_transaction(self, transaction_type, amount):
        try:
            transaction = {
                "type": transaction_type,
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.transactions.append(transaction)
        except Exception as e:
            print(f"Error recording transaction: {e}")

    # Display account transactions
    def show_transactions(self):
        try:
            print(f"Transaction History for Account {self.account_number}:")
            for txn in self.transactions:
                print(f"{txn['date']} - {txn['type']}: ${txn['amount']}")
        except Exception as e:
            print(f"Error displaying transactions: {e}")

    # Convert account data to a dictionary
    def to_dict(self):
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "balance": self.balance,
            "transactions": self.transactions
        }

    # Create a BankAccount object from a dictionary
    @staticmethod
    def from_dict(data):
        account = BankAccount(data["account_number"], data["account_holder"], data["balance"])
        account.transactions = data["transactions"]
        return account

    # Save accounts to a file
    @staticmethod
    def save_accounts(accounts, filename="accounts.json"):
        try:
            with open(filename, "w") as file:
                json.dump([acc.to_dict() for acc in accounts], file, indent=4)
                print("Accounts saved successfully.")
        except Exception as e:
            print(f"Error saving accounts: {e}")

    # Load accounts from a file
    @staticmethod
    def load_accounts(filename="accounts.json"):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    data = json.load(file)
                    return [BankAccount.from_dict(acc) for acc in data]
            return []
        except json.JSONDecodeError:
            print("Error reading the accounts file. The file may be corrupted.")
            return []
        except Exception as e:
            print(f"Error loading accounts: {e}")
            return []

    # Create a new account
    @staticmethod
    def create_account(accounts):
        try:
            account_number = input("Enter Account Number: ")
            account_holder = input("Enter Account Holder Name: ")
            new_account = BankAccount(account_number, account_holder)
            accounts.append(new_account)
            print("Account created successfully.")
        except Exception as e:
            print(f"Error creating account: {e}")


# Main function

def main():
    accounts = BankAccount.load_accounts()
    while True:
        print("\nBanking Application Menu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Show Transactions")
        print("6. Save and Exit")
        choice = input("Choose an option (1-6): ")

        if choice == "1":
            BankAccount.create_account(accounts)
        elif choice == "2":
            acc_number = input("Enter Account Number: ")
            account = next((acc for acc in accounts if acc.account_number == acc_number), None)
            if account:
                try:
                    amount = float(input("Enter amount to deposit: "))
                    account.deposit(amount)
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
            else:
                print("Account not found.")
        elif choice == "3":
            acc_number = input("Enter Account Number: ")
            account = next((acc for acc in accounts if acc.account_number == acc_number), None)
            if account:
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    account.withdraw(amount)
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
            else:
                print("Account not found.")
        elif choice == "4":
            src_number = input("Enter Source Account Number: ")
            target_number = input("Enter Target Account Number: ")
            src_account = next((acc for acc in accounts if acc.account_number == src_number), None)
            target_account = next((acc for acc in accounts if acc.account_number == target_number), None)
            if src_account and target_account:
                try:
                    amount = float(input("Enter amount to transfer: "))
                    src_account.transfer(target_account, amount)
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
            else:
                print("One or both accounts not found.")
        elif choice == "5":
            acc_number = input("Enter Account Number: ")
            account = next((acc for acc in accounts if acc.account_number == acc_number), None)
            if account:
                account.show_transactions()
            else:
                print("Account not found.")
        elif choice == "6":
            BankAccount.save_accounts(accounts)
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


