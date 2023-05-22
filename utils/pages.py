import streamlit as st


def set_page_config(title=""):
    st.set_page_config(
        page_title=title if len(title) > 0 else "PredictHQ Location Insights Demo App",
        page_icon="🪧",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get help": "https://docs.predicthq.com",
            "About": """
                **PredictHQ Location Insights Demo App**

                PredictHQ Technical Documentation can be found at [https://docs.predicthq.com](https://docs.predicthq.com).
            """,
        },
    )
