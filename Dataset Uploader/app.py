import streamlit as st
import plotly.express as px
from pycaret.regression import setup, compare_models, pull, save_model, load_model
import pandas_profiling
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
import os 

def main():
    if os.path.exists('./dataset.csv'):
        df = pd.read_csv('dataset.csv', index_col=None)
    
    with st.sidebar:
        st.image("happy.png")
        st.title("DisplayYourData")
        choice = st.radio("Navigation", ["Update and Download", "Upload","Profiling", "Modelling", "Download"])
        st.info("This application will take a dataset and upload the contents where you can do the following...  \n1. Update your dataset and download it updated \n2. Upload a csv without updating it \n3. Display the contents of the dataset \n4. Automatically train the dataset \n5. Download the trained model")

    if choice == "Upload":
        st.title("Upload Your Dataset")
        file = st.file_uploader("Upload Your Dataset")
        try:
            if file:
                df = pd.read_csv(file, index_col=None)
                df.to_csv('dataset.csv', index=None)
                st.dataframe(df)
                st.write("Dropping missing values")
                df.dropna()
        except:
                st.write("Your dataset cannot be processed, try again")
                st.image("fail.png")

    if choice == "Update and Download":
        st.title("Update/Download")
        st.subheader("Please upload the csv file you would like to update: ")
        file = st.file_uploader("Upload CSV", type=["CSV"])

        if file:
            st.write("Your uploaded CSV: (note, if your CSV is large, only a few rows will be shown) ")
            df = pd.read_csv(file)
            data_top = df.head()
            st.write(data_top)
            st.subheader("Your CSV has the following columns... ")
            col_name = []
            for col in df.columns:
                st.write(col)
                col_name.append(col)
            usr_input = st.text_input("Please enter a new entry separated with a comma for each column")
            total = usr_input.split(',')
            if len(total) != len(df.columns):
                st.write("Incorrect number of columns matched in new entry")
            else:
                st.write("Valid input")
                updated_entry = []
                for entry in total:
                    try:
                        int(entry)
                        updated_entry.append(entry)
                    except:
                        updated_entry.append(entry)
                updated_entry = [updated_entry]
                df = df.append(pd.DataFrame(updated_entry, columns=col_name), ignore_index=True)
                csv = df.to_csv(index=False)
                label = st.text_input("Please enter name for csv file including the .csv")
                if label.endswith(".csv"):
                    clicked = st.download_button("Press to Download", csv, label, mime='text/csv')
                    if clicked:
                        st.image('success.gif')
                else:
                    st.write("Invalid, please try again")

            
        else:
            pass

    if choice == "Profiling":
        st.title("Data analysis on your uploaded dataset")
        st.image("smart.png")
        profile = df.profile_report()
        st_profile_report(profile) 

    if choice == "Modelling":
        chosen_target = st.selectbox('Choose the Target Column', df.columns)
        if st.button('Run Modelling'): 
            setup(df, target=chosen_target, silent=True)
            setup_df = pull()
            st.dataframe(setup_df)
            best_model = compare_models()
            compare_df = pull()
            st.dataframe(compare_df)
            save_model(best_model, 'best_model')
    
    if choice == "Download": 
        with open('best_model.pkl', 'rb') as f: 
            st.download_button('Download Model', f, file_name="best_model.pkl")
main()