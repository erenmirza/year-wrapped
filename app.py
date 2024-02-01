import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.express as px
from forex_python.converter import CurrencyRates

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
    
def days_between(d1, d2):
    return abs((d2 - d1).days)

def get_friendship_start_df(current_user_identifier, current_user_name):
    df = pd.json_normalize(st.secrets['users'])
    df = df[['identifier', 'name', 'friendship_start_date']]
    df = df[df['identifier'] != -1]
    df['days_since_start'] = (pd.to_datetime(datetime.now().date()) - pd.to_datetime(df['friendship_start_date'])).dt.days

    condition = (df['identifier'] == current_user_identifier)

    value_true = True
    value_false = False

    df['current_user_flag'] = np.where(condition, value_true, value_false)

    df['anonymised_names'] = np.where(condition, current_user_name, 'Friend ' + df['identifier'].astype(str))

    return df.sample(frac=1)

# Main function for your app
def main():    
    # Get password input from the user
    password = st.text_input("Enter your password:", type="password")

    # Button to check the password
    if st.button("Submit"):
        user_details = get_user_details(password)
        
        # Check if the password is correct
        if user_details != {}:
            st.success('Password accepted!')
            
            # Wrapped Section
            st.title("Fri-EREN-dship Wrapped")
            st.header(user_details['name'], divider='rainbow')
            st.subheader("We've been friends since...")
            st.header(user_details['friendship_start_date'], divider='blue')
            st.subheader("Which means I've known you for...")
            st.header(f"{days_between(datetime.now().date(), user_details['friendship_start_date'])} days!", divider='green')
            st.subheader("Let's see where that puts you amongst the other folks")
            fig = px.bar(
                get_friendship_start_df(user_details['identifier'], user_details['name'])
                , x="days_since_start"
                , y="anonymised_names"
                , color="current_user_flag"
                , color_discrete_map={
                    True: 'green',
                    False: 'grey'
                }
                , title = "Friendship Lengths Compared"
            )
            st.plotly_chart(fig)
            st.divider()
            st.subheader("However long it's been, we've had some good memories, remember this?")
            st.header(user_details['best_memory'], divider='orange')
            st.subheader("For all your hard work it is being my friend, you win the following award:")
            st.header(user_details['positive_award'], divider='red')
            st.subheader("However, you piss me off from time to time as well. Which is why you've also won:")
            st.header(user_details['negative_award'], divider='gray')
            st.subheader("My message to you as 2023 ends, would be something like:")
            st.header(user_details['personal_message'], divider='rainbow')
            
            # Eren Points Sections
            st.title("Eren Points")
            st.subheader("Current Balance (E*):")
            c = CurrencyRates()
            exchange_rate = c.get_rate('GBP', 'USD')
            st.header(f"{user_details['eren_points_remaining']} E*", divider='blue')
            st.subheader("Current Balance (GBP):")
            gbp_amount = exchange_rate * user_details['eren_points_remaining']
            st.header(f"£{round(gbp_amount, 2)}", divider='green')
            st.subheader("About Eren Points (E*)")
            st.markdown(
                f'''
                    Please take a moment to read and understand the following disclaimer:  
                    #### Monetary Value:  
                    Eren Points are a virtual currency created for the purpose of entertainment among friends and can be exchanged for GBP at the discretion of the participants.  
                    #### Exchange Rate:  
                    The exchange rate between Eren Points and GBP is {exchange_rate}. This rate is subject to change at any time without prior notice.  
                    #### Financial Transaction:  
                    Users acknowledge that transactions involving Eren Points may have financial implications, and the exchange for GBP constitutes a real-world financial transaction.  
                    #### Limited Scope:  
                    Eren Points are intended for use within the context of this website and any associated activities among friends who are aware of the currency's real-world value.  
                    #### Legal Implications:  
                    Users are responsible for complying with any applicable laws and regulations related to the exchange and use of Eren Points. The creators and administrators of this website are not liable for any legal consequences resulting from the use of Eren Points.  
                    #### Not a Registered Currency:  
                    Eren Points are not a registered or government-issued currency. The exchange is facilitated privately among participants.  
                    #### User Agreement:  
                    By using this website and participating in the Eren Points system, users agree to the terms and conditions outlined in this disclaimer. Any disputes arising from Eren Points transactions will be resolved among the involved parties.  
                    #### Financial Risks:  
                    Users are advised to be aware of the financial risks associated with exchanging Eren Points for GBP. The value of Eren Points may fluctuate, and participants should exercise caution.
                    Please carefully review this disclaimer before engaging in any transactions involving Eren Points. If you have any questions or concerns, please contact your local Eren.
                '''
            )
                        
        else:
            st.error("Incorrect password. Please try again.")

# Run the app
if __name__ == "__main__":
    main()
