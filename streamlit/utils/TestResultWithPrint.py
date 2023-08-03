import unittest
import streamlit as st

class TestResultWithPrint(unittest.TextTestResult):
    def startTest(self, test):
        super().startTest(test)
        print("Running:", test._testMethodName)
        st.text(f"Running: {test._testMethodName}")