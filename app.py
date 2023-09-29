import streamlit as st 
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import PandasAI

load_dotenv()

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key


st.set_page_config(page_title="CSV Whisperer", page_icon="📖", layout="wide")
st.title("📖CSV Whisperer📖")
def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"
            "2. Upload a CSV file📄\n"
            "3. Ask a question about the document💬\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "CSV Whisperer allows you to ask questions about your "
            "csv files and get accurate answers utilizing LLM. " 
        )
        st.markdown(
            "This tool is a work in progress.💡 "
            "If you have any feedback or suggestions, please contact me at https://www.linkedin.com/in/petar-popovski/"
            
        )
        st.markdown("---")
        st.markdown("# Privacy")
        st.markdown(
        "I do not save the documents you upload in any DB. ")
        st.markdown(
        "If you are looking for a solution that uses a local LLM (Large Language Model) "
        "please reach out to me to discuss."
        )
        st.markdown("---")
        st.markdown("Made by Petar Popovski")
        st.markdown("---")

sidebar()
def chat_with_csv(df,prompt):
    llm = OpenAI(api_token=st.session_state.get("OPENAI_API_KEY"))
    pandas_ai = PandasAI(llm)
    result = pandas_ai.run(df, prompt=prompt,is_conversational_answer=True)
    print(result)
    return result


#test comment
input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:
        
        col1, col2 = st.columns([1,1])

        with col1:
            st.info("CSV Uploaded Successfully")
            data = pd.read_csv(input_csv)
            st.dataframe(data, use_container_width=True)

        with col2:

            st.info("Chat Below")
            
            input_text = st.text_area("Enter your query")

            if input_text is not None:
                if st.button("Chat with CSV"):
                    st.info("Your Query: "+input_text)
                    result = chat_with_csv(data, input_text)
                    st.success(result)
        
        st.header("Tips for writing queries")
        st.write("1. Ask questions about the data in the CSV file by referencing the column names")
        st.write("2. Prompt the application with a concise requirement of what you want to know")
        st.write("3. If you want to query by some values in the csv file, either tell the application the specific value IS or CONTAINS the value.")

        st.header("Example queries")
        st.info("Tell me the total number of '[SOME PRODUCT]' products sold to [CLIENT] from the csv file.")
        st.info("How much is the total value of the [PRICE SOLD] column where the product is [SOME PRODUCT]?")
        st.info("How much is the total value of the [PRICE SOLD] column where the product is [SOME PRODUCT] and [ORDER DATE] contains 04/12/19?")
        st.info("How many [ORDERS] have been made on [DATE]?")
        st.info("Describe me the uploaded csv file.")
        st.info("What is the average value in the column [COLUMN NAME]?")


