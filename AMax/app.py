import streamlit as st
import pandas as pd
from translation_utils import translate_text

# 1. Set up your Azure Translator credentials
SUBSCRIPTION_KEY = st.secrets["SUBSCRIPTION_KEY"]
ENDPOINT = st.secrets["ENDPOINT"]
REGION = st.secrets["REGION"]


def main():
    # Change the title to a fun version referencing AMax
    st.title("AMax's Magical Translator")

    # A quick welcome message for AMax
    st.write("Hey AMax, ready to make your Excel sheets bilingual (or trilingual) with a single click? Let's roll!")

    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Here's a preview of your uploaded file:", df.head())

            # Let’s pick which column to translate
            columns = df.columns.tolist()
            selected_column = st.selectbox("Which column needs a linguistic glow-up?", columns)

            # Choose target language
            language_map = {"English": "en", "Simplified Chinese": "zh-Hans", "Traditional Chinese": "zh-Hant"}
            target_language = st.selectbox("Target Language?", list(language_map.keys()))

            if st.button("Abracadabra — Translate!"):
                # Generate a new column name
                translated_col_name = f"{selected_column}_translated_{language_map[target_language]}"

                df[translated_col_name] = df[selected_column].apply(
                    lambda text: translate_text(
                        text,
                        SUBSCRIPTION_KEY,
                        ENDPOINT,
                        REGION,
                        to_language=language_map[target_language]
                    ) if pd.notnull(text) else None
                )

                st.success("Boom! Translation complete.")
                st.write(df.head())

                # Provide a download option
                st.download_button(
                    label="Download Your Magical Translation",
                    data=to_excel_binary(df),
                    file_name="translated_spreadsheet.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Oops, something went sideways: {e}")

def to_excel_binary(df):
    """Utility function to convert a DataFrame to Excel bytes for download."""
    from io import BytesIO
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.save()
    return output.getvalue()

if __name__ == "__main__":
    main()
