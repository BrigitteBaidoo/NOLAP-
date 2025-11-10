import random

user_database = {
    "1234567890": {"pin": "1111", "balance": 1000.0},
    "9876543210": {"pin": "2222", "balance": 500.0},
    "5551234567": {"pin": "3333", "balance": 2000.0}
}

def validate_telephone_number(telephone_num):
    return len(telephone_num) == 10 and telephone_num.isdigit()

def validate_pin(pin):
    return len(pin) == 4 and pin.isdigit()

def generate_token():
    return str(random.randint(100000, 999999))

def authenticate_user(telephone_num, pin):
    user = user_database.get(telephone_num)
    return user and user["pin"] == pin

def get_user_balance(telephone_num):
    return user_database[telephone_num]["balance"]

def update_user_balance(telephone_num, amount):
    user_database[telephone_num]["balance"] += amount

def change_pin(telephone_num, new_pin):
    user_database[telephone_num]["pin"] = new_pin

def transfer_money(sender_num, recipient_num, amount, reference):
    fee = 0.0075 * amount
    if amount >= 2000:
        fee = 15
    total = amount + fee
    if total > user_database[sender_num]["balance"]:
        return False, "Insufficient balance"
    user_database[sender_num]["balance"] -= total
    user_database[recipient_num]["balance"] += amount
    return True, "Transfer successful"

def buy_airtime(telephone_num, amount):
    """Buy airtime"""
    if amount > user_database[telephone_num]["balance"]:
        return False, "Insufficient balance"
    user_database[telephone_num]["balance"] -= amount
    return True, "Airtime purchase successful"

def withdraw_cash(telephone_num, amount):
    """Withdraw cash"""
    fee = 0.01 * amount
    total = amount + fee
    if total > user_database[telephone_num]["balance"]:
        return False, "Insufficient balance"
    user_database[telephone_num]["balance"] -= total
    token = generate_token()
    return True, token

def deposit_cash(telephone_num, amount):
    """Deposit cash"""
    user_database[telephone_num]["balance"] += amount
    return True, "Deposit successful"

def main():
    print("Welcome to NOLAP Pay!")
    while True:
        telephone_num = input("Enter your telephone number: ")
        if validate_telephone_number(telephone_num):
            break
        else:
            print("Invalid telephone number. Please enter a 10-digit number.")

    if telephone_num not in user_database:
        print("Sign up")
        while True:
            pin = input("Create your PIN (4 digits): ")
            if validate_pin(pin):
                user_database[telephone_num] = {"pin": pin, "balance": 0.0}
                break
            else:
                print("PIN must be 4 digits long.")

    while True:
        pin = input("Enter your PIN: ")
        if authenticate_user(telephone_num, pin):
            break
        else:
            print("Invalid PIN. Please try again.")

    while True:
        code = input("Enter code: ")
        if code == "*1145#":
            break
        else:
            print("Invalid code. Please try again.")

    while True:
        print("1. Transfer Money")
        print("2. Buy Airtime (Self)")
        print("3. Withdraw & Deposit")
        print("4. Check Balance")
        print("5. Change PIN")
        print("0. Exit")
        while True:
            try:
                choice = int(input("Enter choice: "))
                if 0 <= choice <= 5:
                    break
                else:
                    print("Invalid choice. Please enter a number between 0 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        if choice == 1:
            while True:
                recipient_num = input("Enter recipient telephone number: ")
                if validate_telephone_number(recipient_num):
                    break
                else:
                    print("Invalid telephone number. Please enter a 10-digit number.")
            while True:
                try:
                    amount = float(input("Enter amount to transfer: "))
                    if amount > 0:
                        break
                    else:
                        print("Invalid amount. Please enter a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            reference = input("Enter reference: ")
            success, message = transfer_money(telephone_num, recipient_num, amount, reference)
            print(message)
            if success:
                print(f"New balance: {user_database[telephone_num]['balance']}")

        elif choice == 2:
            while True:
                try:
                    amount = float(input("Enter amount to buy airtime: "))
                    if amount > 0:
                        break
                    else:
                        print("Invalid amount. Please enter a positive number.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            success, message = buy_airtime(telephone_num, amount)
            print(message)
            if success:
                print(f"New balance: {user_database[telephone_num]['balance']}")

        elif choice == 3:
            print("1. Withdraw")
            print("2. Deposit")
            while True:
                try:
                    sub_choice = int(input("Enter choice: "))
                    if 1 <= sub_choice <= 2:
                        break
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            if sub_choice == 1:
                while True:
                    try:
                        amount = float(input("Enter amount to withdraw: "))
                        if amount > 0:
                            break
                        else:
                            print("Invalid amount. Please enter a positive number.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                success, message = withdraw_cash(telephone_num, amount)
                if success:
                    print(f"Withdrawal successful. Token: {message}")
                    print(f"New balance: {user_database[telephone_num]['balance']}")
                else:
                    print(message)
            elif sub_choice == 2:
                while True:
                    try:
                        amount = float(input("Enter amount to deposit: "))
                        if amount > 0:
                            break
                        else:
                            print("Invalid amount. Please enter a positive number.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                success, message = deposit_cash(telephone_num, amount)
                print(message)
                print(f"New balance: {user_database[telephone_num]['balance']}")

        elif choice == 4:
            print(f"Your balance is 0.0")

        elif choice == 5:
            old_pin = input("Enter old PIN: ")
            if old_pin == user_database[telephone_num]["pin"]:
                while True:
                    new_pin = input("Enter new PIN (4 digits): ")
                    if validate_pin(new_pin):
                        change_pin(telephone_num, new_pin)
                        print("PIN changed successfully")
                        break
                    else:
                        print("PIN must be 4 digits long.")
            else:
                print("Invalid old PIN")

        elif choice == 0:
            print("Thank you for using NOLAP Pay!")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()


