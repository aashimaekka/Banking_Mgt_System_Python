import streamlit as st
from bank import Bank  # import your Bank class

# Streamlit Banking App
st.set_page_config(page_title="Banking System", layout="centered")
st.title("Banking System with Streamlit")

# Instantiate
user = Bank()

menu = ["Create Account", "Deposit Money", "Withdraw Money", 
        "Fetch Holder Details", "Update Details", "Delete Account"]
choice = st.sidebar.selectbox("Select Action", menu)

if choice == "Create Account":
    st.subheader("Create a New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    address = st.text_area("Address")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    pin = st.text_input("PIN (4 digits)", type="password")

    if st.button("Create Account"):
        if age < 18:
            st.error("SORRY, Account cannot be created (must be 18+).")
        elif not pin.isdigit() or len(pin) != 4:
            st.error("Invalid PIN. It must be exactly 4 digits.")
        else:
            info = {
                "name": name, "age": age, "gender": gender, "address": address,
                "phone": phone, "email": email, "username": username,
                "password": password, "pin": int(pin),
                "accountNo": Bank._Bank__accountgenerate(),
                "balance": 0
            }
            Bank.data.append(info)
            Bank._Bank__update()
            st.success("Account created successfully!")
            st.json(info)

elif choice == "Deposit Money":
    st.subheader("Deposit Money")
    accNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Deposit Amount (₹)", min_value=1, step=1)

    if st.button("Deposit"):
        userdata = [u for u in Bank.data if u['accountNo'] == accNo and str(u['pin']) == pin]
        if not userdata:
            st.error("Sorry, no account found.")
        elif amount > 10000:
            st.error("Deposit limit exceeded (Max ₹10,000).")
        else:
            userdata[0]['balance'] += amount
            Bank._Bank__update()
            st.success(f"Deposit successful! Current balance: ₹{userdata[0]['balance']}")

elif choice == "Withdraw Money":
    st.subheader("Withdraw Money")
    accNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Withdraw Amount (₹)", min_value=1, step=1)

    if st.button("Withdraw"):
        userdata = [u for u in Bank.data if u['accountNo'] == accNo and str(u['pin']) == pin]
        if not userdata:
            st.error("Sorry, no account found.")
        elif amount > userdata[0]['balance']:
            st.error("Invalid amount or insufficient balance.")
        else:
            userdata[0]['balance'] -= amount
            Bank._Bank__update()
            st.success(f" Withdrawal successful! Current balance: ₹{userdata[0]['balance']}")

elif choice == "Fetch Holder Details":
    st.subheader("📋 Account Details")
    accNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show Details"):
        userdata = [u for u in Bank.data if u['accountNo'] == accNo and str(u['pin']) == pin]
        if not userdata:
            st.error("Sorry, no account found.")
        else:
            st.json(userdata[0])

elif choice == "Update Details":
    st.subheader(" Update Details")
    accNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Fetch Account"):
        userdata = [u for u in Bank.data if u['accountNo'] == accNo and str(u['pin']) == pin]
        if not userdata:
            st.error("Sorry, no account found.")
        else:
            account = userdata[0]
            name = st.text_input("Name", account['name'])
            email = st.text_input("Email", account['email'])
            username = st.text_input("Username", account['username'])
            password = st.text_input("Password", account['password'])
            phone = st.text_input("Phone", account['phone'])
            address = st.text_area("Address", account['address'])
            new_pin = st.text_input("New PIN (4 digits)", "")

            if st.button("Update Now"):
                account.update({"name": name, "email": email, "username": username,
                                "password": password, "phone": phone, "address": address})
                if new_pin.isdigit() and len(new_pin) == 4:
                    account['pin'] = int(new_pin)
                Bank._Bank__update()
                st.success("Details updated successfully!")

elif choice == "Delete Account":
    st.subheader("Delete Account")
    accNo = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        userdata = [u for u in Bank.data if u['accountNo'] == accNo and str(u['pin']) == pin]
        if not userdata:
            st.error("Sorry, no account found.")
        else:
            Bank.data.remove(userdata[0])
            Bank._Bank__update()
            st.success("Account deleted successfully.")
