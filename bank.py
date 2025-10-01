import json
import random
import string
from pathlib import Path

class Bank:
    database = Path("bank_data.json")
    data = []  # in-memory storage

    # Load data from file if it exists
    try:
        if database.exists():
            with open(database, 'r') as fs:
                data = json.load(fs)
        else:
            print("No existing database found, starting fresh...")
    except Exception as err:
        print(f"An exception occurred while loading data: {err}")

    @classmethod
    def __update(cls):
        """Write current in-memory data to JSON file"""
        with open(cls.database, 'w') as fs:
            json.dump(Bank.data, fs, indent=4)

    @classmethod
    def __accountgenerate(cls):
        """Generate a random account number"""
        alpha = random.choices(string.ascii_uppercase, k=3)
        num = random.choices(string.digits, k=5)
        acc_no = "".join(alpha + num)
        return acc_no

    def Createaccount(self):
        try:
            age = int(input("Age: "))
            if age < 18:
                print("SORRY, Account cannot be created (must be 18+).")
                return

            pin = input("Pin (4 digits): ")
            if not pin.isdigit() or len(pin) != 4:
                print("Invalid PIN. It must be exactly 4 digits.")
                return

            info = {
                "name": input("Name: "),
                "age": age,
                "gender": input("Gender: "),
                "address": input("Address: "),
                "phone": input("Phone: "),
                "email": input("Email: "),
                "username": input("Username: "),
                "password": input("Password: "),
                "pin": int(pin),
                "accountNo": Bank.__accountgenerate(),
                "balance": 0
            }

            Bank.data.append(info)
            Bank.__update()

            print("\n✅ Account created successfully!")
            for k, v in info.items():
                print(f"{k}: {v}")
            print("Note: Recheck your details. Report any incorrect data to the Branch Manager.")

        except Exception as e:
            print(f"Error while creating account: {e}")

    def __find_user(self, accNo, pin):
        """Helper to find a user by account number and PIN"""
        return [u for u in Bank.data if u['accountNo'] == accNo and u['pin'] == pin]

    def Deposit(self):
        accNo = input("Enter your account number: ")
        try:
            pin = int(input("Enter your pin: "))
        except:
            print("Invalid pin.")
            return

        userdata = self.__find_user(accNo, pin)
        if not userdata:
            print("Sorry, no account found.")
            return

        try:
            amount = int(input("Enter the deposit amount in INR: "))
            if amount <= 0:
                print("Invalid amount.")
                return
            if amount > 10000:
                print("❌ Deposit limit exceeded (Max ₹10,000).")
                return

            userdata[0]['balance'] += amount
            Bank.__update()
            print(f"✅ Deposit successful! Current balance: ₹{userdata[0]['balance']}")
        except:
            print("Invalid input.")

    def Withdraw(self):
        accNo = input("Enter your account number: ")
        try:
            pin = int(input("Enter your pin: "))
        except:
            print("Invalid pin.")
            return

        userdata = self.__find_user(accNo, pin)
        if not userdata:
            print("Sorry, no account found.")
            return

        try:
            amount = int(input("Enter withdrawal amount in INR: "))
            if amount <= 0 or amount > userdata[0]['balance']:
                print("❌ Invalid amount or insufficient balance.")
                return

            userdata[0]['balance'] -= amount
            Bank.__update()
            print(f"✅ Withdrawal successful! Current balance: ₹{userdata[0]['balance']}")
        except:
            print("Invalid input.")

    def Showdetails(self):
        accNo = input("Enter your account number: ")
        try:
            pin = int(input("Enter your pin: "))
        except:
            print("Invalid pin.")
            return

        userdata = self.__find_user(accNo, pin)
        if not userdata:
            print("Sorry, no account found.")
            return

        print("\n📋 Account Details")
        for k, v in userdata[0].items():
            print(f"{k}: {v}")

    def Updatedetails(self):
        accNo = input("Enter your account number: ")
        try:
            pin = int(input("Enter your pin: "))
        except:
            print("Invalid pin.")
            return

        userdata = self.__find_user(accNo, pin)
        if not userdata:
            print("Sorry, no account found.")
            return

        print("\nYou cannot change Age, Account No, and Balance.\n")
        newdata = userdata[0].copy()

        for field in ["name", "email", "username", "password", "phone", "address"]:
            val = input(f"Enter new {field} (press Enter to skip): ")
            if val.strip():
                newdata[field] = val

        pin_input = input("Enter new 4-digit pin (press Enter to skip): ")
        if pin_input.strip():
            if pin_input.isdigit() and len(pin_input) == 4:
                newdata['pin'] = int(pin_input)
            else:
                print("Invalid pin. Keeping old pin.")

        index = Bank.data.index(userdata[0])
        Bank.data[index] = newdata
        Bank.__update()

        print("✅ Details updated successfully.")

    def Delete(self):
        accNo = input("Enter your account number: ")
        try:
            pin = int(input("Enter your pin: "))
        except:
            print("Invalid pin.")
            return

        userdata = self.__find_user(accNo, pin)
        if not userdata:
            print("Sorry, no account found.")
            return

        check = input("Are you sure you want to delete your account? (y/n): ")
        if check.lower() != 'y':
            print("❌ Account deletion cancelled.")
            return

        Bank.data.remove(userdata[0])
        Bank.__update()
        print("✅ Account deleted successfully.")


def main():

    user = Bank()

    while True:
        print("\n===== Banking System =====")
        print("1. Create account")
        print("2. Deposit money")
        print("3. Withdraw money")
        print("4. Fetch holder details")
        print("5. Update details")
        print("6. Delete the account")
        print("7. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            user.Createaccount()
        elif choice == 2:
            user.Deposit()
        elif choice == 3:
            user.Withdraw()
        elif choice == 4:
            user.Showdetails()
        elif choice == 5:
            user.Updatedetails()
        elif choice == 6:
            user.Delete()
        elif choice == 7:
            print("👋 Exiting... Thank you for using our banking system.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
