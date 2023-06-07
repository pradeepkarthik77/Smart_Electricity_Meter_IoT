# Smart Electricity Monitor
### Smart Electricity Monitor is a IoT project that is intended to automate the manual Electricity Bill calculation done in the EB department in India. This Documentation covers the detailed implementation of this project.

## [Visit Our Hosted Website](https://smartelectricitymonitor.streamlit.app/)

## Problem Statement
As of now, the Readings for the total units consumed is documented manually. A Electrician visits every household once in a month to collecte the monthly readings and if the owner is not available at the particular day, It is the owner's responsibility to visit the local EB office to provide the readings for the month or else the current month's Billing is coupled with the previous month which increases the amount payable since the per unit cost increases with the increase in number of units consumed per month.

## Solution Proposed
The proposed solution is to automate the Readings collection process by using a IoT enabled device to periodically update the readings to the cloud so that the readings calculation and payment can be done in online. Along with this the proposed project provides other features for managing power usage efficiently. 

## Features
1. Automatic Power Readings from the Household mains and storage in AWS DynamoDB
2. Automatic User Alert and ShutDown in case of abnormal voltage spikes
3. Estimated bill calculation by predicting the future readings using ML
4. Live Readings Display
5. Control your devices remotely when you've left them ON
6. Visualize your Daily and Monthly Power usage to gain insights

## Tech Stack Used:
1. Arduino IDE 
2. AWS Iot Core
3. AWS Lambda Functions
4. AWS DynamoDB
5. AWS API Gateway
6. Streamlit Cloud

## HardWare Requirements:
1. ESP32 Microcontroller - 1
2. ZMPT101b Voltage sensor - 3
3. ACS712 current sensor - 3
4. Relay module - 3
5. Jumper wires
6. Breadboard

## Implementation:
1. **Phase 1: HardWare Setup**: Setup the connections with ESP32 and sensors to read voltage,current and power readings along with Relay module for controlling the devices remotely. Make use of the [EMONLib Library](https://github.com/openenergymonitor/EmonLib) for reading data.

2. **Phase 2: Data Collection and Storage**: Register the ESP32 device as a IoT thing in AWS IoT core and write a rule to route the incoming data to a lambda function that performance EDA and adds attributes like date and time before the storing the values into AWS DynamoDBs. (The tables in the DynamoDBs are discussed in detail later in this documentation).

3. **Phase 3: Creating API Endpoints for Data Retrival**: Now in order to fetch the data from the DBs to the frontend, we use microservices architechture to write multiple lambda functions for Data Retrival. (Functionality of each lambda function are discussed in detail later in this documentation) after creating lambda functions, create a API Endpoint for each functions. Here's an amazing [video](https://youtu.be/lss7T0R019M) for hosting a endpoint.

4. **Phase 4: Creating a User Interface**: Create a Website using the [Streamlit Package](https://docs.streamlit.io/) for Visualizing Collected data, Displaying Live Readings, Remote Control of Devices and Electricity Bill prediction for the upcoming weeks and months.

## AWS Overview:
![AWS Architecture Reference](https://github.com/pradeepkarthik77/Smart_Electricity_Meter_IoT/assets/77573751/fea75793-bacd-4368-88ce-f2a939ff7c48)


## DynamoDB tables:
1. meter_data: A DB that consists of all the incoming data from the IoT thing. Attributes: date_time,date,time,voltage_main,current_main,power_main,voltage_dev1,current_dev1,power_dev1,voltage_dev2,current_dev2,power_dev2.

2. date_power_data: A DB that consists of the aggregated power usage for each day of the month. (This DB is primarily used for Electricity Bill predictiona and data visualizations). Attributes: date, power_used

3. live_data_table: A DB that contains the live readings incoming from the device and the live status for each devices (on/off). This Db is used for displaying live readings and for Remote device control. Attributes:	dev1_status,dev2_status,live_current_dev1,live_current_dev2,live_current_main,live_power_dev1,live_power_dev2,live_power_main,live_voltage_dev1,live_voltage_dev2,live_voltage_main,main_status.

## AWS Lambda Functions:
1. New_EDA_Incoming_IOT: A lambda function to store the incoming data into the 3 DynamoDB tables and also to implement User Alert and automatic shutdown in case of Abnormal Voltage Spike.

2. Fetch_For_Prediction: A lambda function to return the user's past power_consumption for training the ML Prediction model.

3. Return_Live_data: A lambda function to return the live readings from the live_data_table.

4. Return_Monthly_Usage: A lambda function to return the day-wise power consumption for the current month for data visualization in the frontend.

5. Return_Yearly_Usage: A lambda function to return the month-wise power consumption for the current year for data visualization in the frontend.

6. Publish_To_Client: A lambda function to turn off devices remotely based on the requests received from the frontend.

## Frontend Implementation:
1. Import the streamlit package into your python environment to start building websites in simple steps.
2. Hit the already created endpoint and use the retrived data to display Data Visualizations, Live Readings, Device Status to the user.
3. The ML model (Prophet for Time-Series Prediction) is lightweight and is hence run on the frontend.
4. Add a requirements.txt file to your project speicifying the requirements for your python package.
5. Host your project by creating a GitHub repo and Register your project in [Streamlit Cloud](https://streamlit.io/cloud) for hosting your website free of cost!

## Issues and Pull Requests:
In case you have any improvement/suggestions, Create a Pull Request or if you have any clarifications, feel free to open a issue or reach out to any of the Collaborators to get it clarified.
