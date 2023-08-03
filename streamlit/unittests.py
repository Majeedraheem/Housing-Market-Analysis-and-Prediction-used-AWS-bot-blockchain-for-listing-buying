import streamlit as st
import unittest
from utils.StringIOWithWriteln import StringIOWithWriteln
from utils.TestResultWithPrint import TestResultWithPrint
from TestMyFunctions_Chatbot import TestMyFunctions_Chatbot
from TestMyFunctions_Trends import TestMyFunctions_Trends

def run_tests(*test_cases):
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for test_case in test_cases:
        tests = loader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)

    runner = unittest.TextTestRunner()

    # Stream the test output to a string
    stream = StringIOWithWriteln()
    runner.resultclass = TestResultWithPrint
    runner.stream = stream
    runner.run(suite)

    # Get the test results from the string
    stream.seek(0)
    test_result = stream.read()

    return test_result

def render_page():
    st.title("Unit Tests")

    results = run_tests(TestMyFunctions_Chatbot, TestMyFunctions_Trends)

    # Display the test results
    st.text(results)

