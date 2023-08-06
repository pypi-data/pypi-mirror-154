import streamlit.components.v1 as components
import streamlit as st
import os


parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_wallet_connect = components.declare_component("wallet_connect", path=build_dir)


def get_button(label, key=None):
    return _wallet_connect(label=label, default="not", key=key)

def connect(label, show_status=False, key=None):
    wallet_button = get_button(label="wallet", key="wallet")
    if show_status:
        st.write(f"Wallet {wallet_button} connected.")
    return wallet_button