import streamlit as st
import googlemaps


def get_api_key():
    return st.secrets["google_api_key"]


def places_autocomplete(address, session_token):
    gmaps = googlemaps.Client(key=get_api_key())

    result = gmaps.places_autocomplete(
        address,
        session_token=session_token,
    )
    return result


def get_place_details(place_id, session_token):
    gmaps = googlemaps.Client(key=get_api_key())

    result = gmaps.place(
        place_id,
        session_token=session_token,
    )
    return result
