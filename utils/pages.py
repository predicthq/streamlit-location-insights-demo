import streamlit as st
import streamlit.components.v1 as components


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

    # Testing adding Heap Analytics
    components.html(
        """
        <script type="text/javascript">
            window.heap=window.heap||[],heap.load=function(e,t){window.heap.appid=e,window.heap.config=t=t||{};var r=document.createElement("script");r.type="text/javascript",r.async=!0,r.src="https://cdn.heapanalytics.com/js/heap-"+e+".js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(r,a);for(var n=function(e){return function(){heap.push([e].concat(Array.prototype.slice.call(arguments,0)))}},p=["addEventProperties","addUserProperties","clearEventProperties","identify","resetIdentity","removeEventProperty","setEventProperties","track","unsetEventProperty"],o=0;o<p.length;o++)heap[p[o]]=n(p[o])};
            heap.load("2099083646");
        </script>
        """
    )
