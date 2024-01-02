import streamlit as st
import json

# Function to check the entered password
def get_user_details(entered_password):
    passwords = []
    
    for user in st.secrets.users:
        passwords.append(user['password'])

    if entered_password in passwords:
        user_index = passwords.index(entered_password)
        return st.secrets.users[user_index]
    else:
        return {}

# Main function for your app
def main():
    st.title("Fri-EREN-dship Wrapped")
    
    # Get password input from the user
    password = st.text_input("Enter your password:", type="password")

    # Button to check the password
    if st.button("Submit"):
        user_details = get_user_details(password)
        
        # Check if the password is correct
        if user_details != {}:
            st.success('Password accepted!')
            st.write(user_details)

        else:
            st.error("Incorrect password. Please try again.")

# Run the app
if __name__ == "__main__":
    main()
