import streamlit as st
import matplotlib.pyplot as plt
import requests
import math
import time
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
datac = pd.read_csv('results.csv', parse_dates=['date'], dayfirst=True)

class Solution:

    def __init__(self):
        pass

        
    def monthly_stats(self):

        url = 'https://9768paaqk9.execute-api.us-east-1.amazonaws.com/InitStage/fetch_monthly_data'

        response = requests.post(url, json={})

        x_labels = []
        y_values = []

        if response.status_code == 200:
            response_data = response.json()
            
            length = len(response_data["values"])

            x_labels = [i for i in range(1,length+1)]

            y_values = response_data["values"]

        # Create the bar chart
        plt.bar(x_labels, y_values)

        # Set x-axis and y-axis labels
        plt.xlabel('X-axis Label')
        plt.ylabel('Y-axis Label')

        # Rotate x-axis labels if needed
        plt.xticks(rotation=90)

        # Create the bar chart
        fig, ax = plt.subplots()
        ax.bar(x_labels, y_values)

        # Set x-axis and y-axis labelsand title
        ax.set_xlabel('Days of the month')
        ax.set_ylabel('Power consumed (in watts)')
        ax.set_title('Monthly Stats')

        # Display the chart in Streamlit
        st.pyplot(fig)
    
    def yearly_stats(self):

        st.header("Yearly Power Usage")

        url = 'https://9768paaqk9.execute-api.us-east-1.amazonaws.com/NextStage/fetch_monthly_data/fetch_years'

        response = requests.post(url, json={})

        x_labels = []
        y_values = []

        if response.status_code == 200:
            response_data = response.json()
            
            length = len(response_data["values"])

            x_labels = [i for i in range(1,length+1)]

            y_values = response_data["values"]

        # Create the bar chart
        plt.bar(x_labels, y_values)

        # Set x-axis and y-axis labels
        plt.xlabel('X-axis Label')
        plt.ylabel('Y-axis Label')

        # Rotate x-axis labels if needed
        plt.xticks(rotation=90)

        # Create the bar chart
        fig, ax = plt.subplots()
        ax.bar(x_labels, y_values)

       # Set x-axis and y-axis labelsand title
        ax.set_xlabel('Months')
        ax.set_ylabel('Power consumed (in watts)')
        ax.set_title('Yearly Stats')

        # Display the chart in Streamlit
        st.pyplot(fig)
    
    def getlive(self):
        url = 'https://9768paaqk9.execute-api.us-east-1.amazonaws.com/NextStage/fetch_monthly_data/fetch_live'
        response = requests.post(url, json={})

        response_data = response.json()

        volt_main = response_data["live_voltage_main"]
        curr_main = response_data["live_current_main"]
        power_main = response_data["live_power_main"]

        return [volt_main,curr_main,power_main]

    def getstatus(self):
        url = 'https://9768paaqk9.execute-api.us-east-1.amazonaws.com/NextStage/fetch_monthly_data/fetch_live'
        response = requests.post(url, json={})

        response_data = response.json()

        main_stat = response_data["main_status"]
        dev1_stat = response_data["dev1_status"]
        dev2_stat = response_data["dev2_status"]

        return [main_stat,dev1_stat,dev2_stat]

    
    def live_stats(self):

        st.header("Live Reading")
        
        col1, col2,col3 = st.columns(3)

        with col1:
            widget_container1 = st.empty()
        
        with col2:
            widget_container2 = st.empty()
        
        with col3:
            widget_container3 = st.empty()

        while True:
            # Update the dynamic widget every 10 seconds
            widget_value = self.getlive() # Replace this with your code to get the dynamic widget value
            
            # Update the dynamic widget in the container

            volt_main = widget_value[0]
            curr_main = widget_value[1]
            power_main = widget_value[2]

            col1, col2,col3 = st.columns(3)

            with col1:
                widget_container1.metric(label="Voltage", value=volt_main, delta="V")
            
            with col2:
                widget_container2.metric(label="Current", value=curr_main, delta="A")
            
            with col3:
                widget_container3.metric(label="Power", value=power_main, delta="Watts")
            
            # Wait for 10 seconds before updating the widget again
            time.sleep(5)
    
    def hit_change(self,vals,status):

        url = 'https://9768paaqk9.execute-api.us-east-1.amazonaws.com/NextStage/fetch_monthly_data/send_to_client'

        if vals == 1:
            # hit api
            response = requests.post(url, json={"value":1,"stats":status})
        
        if vals == 2:
            #hit api
            response = requests.post(url, json={"value":2,"stats":status})
        
        if vals == 3:
            #hit api
            response = requests.post(url, json={"value":3,"stats":status})

    def predict_value(self):

        url = "https://9768paaqk9.execute-api.us-east-1.amazonaws.com/NextStage/fetch_monthly_data/-fetch_for_pred"

        st.header("Predicted Power Usage and Electricity Billing for next month")

        response = requests.post(url, json={})
        response_data = response.json()

        datas = response_data["values"]

        datac.columns = ['ds', 'y']

        # Convert the data to a Pandas DataFrame
        df = pd.DataFrame(datac)
        df.columns = ['ds', 'y']

        # Step 2: Create and fit the Prophet model
        model = Prophet()
        model.fit(df)

        # Step 3: Generate future dates for prediction
        future_dates = model.make_future_dataframe(periods=30, freq='D')  # Predicting 30 days from the last date in the dataset

        # Step 4: Make predictions
        forecast = model.predict(future_dates)

        # Step 5: Extract the predicted power consumption for the remaining days
        predicted_power = forecast['yhat'].iloc[-30:]  # Get the last 30 predicted values

        # Step 6: Calculate the total power consumption in watts and kilowatt-hours (kWh)
        total_power_consumption_watts = predicted_power.sum()
        total_power_consumption_watts = round(total_power_consumption_watts, 2)

        total_power_consumption_kWh = total_power_consumption_watts / 3600000 # Convert from watts to kilowatt-hours (kWh)

        # Step 7: Calculate the charges based on the consumption
        charges = 0  # Initialize charges variable

        # Calculate charges for consumption less than or equal to 500 units
        if total_power_consumption_kWh <= 500:
            if total_power_consumption_kWh <= 100:
                charges = 0
            elif total_power_consumption_kWh <= 200:
                charges = 2.25 * (total_power_consumption_kWh - 100)
            elif total_power_consumption_kWh <= 400:
                charges = 2.25 * 100 + 4.5 * (total_power_consumption_kWh - 200)
            else:
                charges = 2.25 * 100 + 4.5 * 200 + 6 * (total_power_consumption_kWh - 400)
        else:
            charges = 2.25 * 100 + 4.5 * 200 + 6 * 100  # Charges up to 500 units
            
            # Calculate charges for consumption more than 500 units
            if total_power_consumption_kWh <= 600:
                charges += 8 * (total_power_consumption_kWh - 500)
            elif total_power_consumption_kWh <= 800:
                charges += 8 * 100 + 9 * (total_power_consumption_kWh - 600)
            elif total_power_consumption_kWh <= 1000:
                charges += 8 * 100 + 9 * 200 + 10 * (total_power_consumption_kWh - 800)
            else:
                charges += 8 * 100 + 9 * 200 + 10 * 200 + 11 * (total_power_consumption_kWh - 1000)
        
        col1, col2 = st.columns(2)

        with col1:
            widget_container1 = st.empty()
            widget_container1.metric(label="Predicted Power usage", value=total_power_consumption_watts, delta="Watts")
        
        with col2:
            widget_container2 = st.empty()
            widget_container2.metric(label="Predicted Electricity Bill", value=charges, delta="Rupees")
        
        
        week1 = round(forecast['yhat'].iloc[-7:].sum(),2)
        week2 = round(forecast['yhat'].iloc[-14:-7].sum(),2)
        week3 = round(forecast['yhat'].iloc[-21:-14].sum(),2)
        week4 = round(forecast['yhat'].iloc[-28:-21].sum(),2)

        st.header("Weekly Prediction for the next month")

        st.metric(label="Week 1",value = week1,delta="watts")
        st.metric(label="Week 2",value = week2,delta="watts")
        st.metric(label="Week 3",value = week3,delta="watts")
        st.metric(label="Week 4",value = week4,delta="watts")


    def control_device(self):

        st.header("Device Control")

        # Update the dynamic widget every 10 seconds
        widget_value = self.getstatus() # Replace this with your code to get the dynamic widget value
        
        # Update the dynamic widget in the container

        main_stats = widget_value[0] == 1            
        dev1_stat = widget_value[1] == 1
        dev2_stat = widget_value[2] == 1

        main_val =  st.checkbox("Main Board Power",value=main_stats,key="main")
        
        dev1_val =  st.checkbox("device 1 Power",value=dev1_stat,key="dev1")
        
        dev2_val = st.checkbox("Device 2 Power",value=dev2_stat,key="dev2")
        
        if st.button("Apply Changes"):

            if main_val != main_stats:
                self.hit_change(1,main_val)

            if dev1_val != dev1_stat:
                self.hit_change(2,dev1_val)
            
            if dev2_val != dev2_stat:
                self.hit_change(3,dev2_val)



        
        
    def home(self):
        st.markdown("# Smart Electricity Monitor")
        
        st.header("Monthly Power Usage:")

        self.monthly_stats()

        self.yearly_stats()
    



if __name__=="__main__":

    s = Solution()

    page_names_to_funcs = {
        "Data Visualizations": s.home,
        "Live Data": s.live_stats,
        "Control Device": s.control_device,
        "Predict Value": s.predict_value
    }
    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()