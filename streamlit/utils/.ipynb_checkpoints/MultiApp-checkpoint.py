import streamlit as st

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Add new applications/pages."""
        self.apps.append({"title": title, "function": func})

    def run(self):
        st.sidebar.subheader("Page selection")

        app = st.sidebar.selectbox(
            'Navigation',
            self.apps,
            format_func=lambda app: app['title']
        )

        # Run the app.
        app['function']()



