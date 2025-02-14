import os
import sys

from loguru import logger
import streamlit as st
import streamlit_authenticator as stauth

from app.constants import EnvConfig


st.set_page_config(
    page_title="SOF-Prototyp",
    layout="centered",
)

authenticator = stauth.Authenticate(os.environ.get(EnvConfig.AUTH_CONFIG_FILE.value))


if __name__ == "__main__":
    try:
        # --- AUTH ---
        authenticator.login(
            fields={
                "Form name": "Sign in",
                "Username": "Benutzername",
                "Password": "Passwort",
                "Login": "Anmelden",
            }
        )

        if st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")

        if st.session_state["authentication_status"]:
            st.write(f"Welcome *{st.session_state['name']}*")

            from app.ui import main

            main()

    except KeyboardInterrupt:
        logger.info("Shutting Down: Process interrupeted")
    except Exception:
        logger.exception("Shutting Down: Exception in main process")
        sys.exit(0)
