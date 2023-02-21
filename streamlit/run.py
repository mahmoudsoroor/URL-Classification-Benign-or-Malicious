import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import pickle
import import_ipynb
import function_features
import pickle
import streamlit as st
import time
from PIL import Image
st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt


class TimerError(Exception):
     """A custom exception used to report errors in use of Timer class"""
 
class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        return (f"Elapsed time: {elapsed_time:0.4f} seconds")

if __name__ == '__main__':
    
				
			st.set_page_config(page_title="URL Classification Benign or Malicious", page_icon=":guardsman:", layout="wide" ,initial_sidebar_state="auto")
			
			st.markdown("<h1 style='text-align: center; color: black;'>URL Classification Benign or Malicious</h1>", unsafe_allow_html=True)
					
				
			st.write("_______________")
			st.markdown("<p style='color: black;'>Different Types of URL's</p>", unsafe_allow_html=True)
			st.markdown("<ul style='color: blackn;'><li>Benign</li><li>Malicious</li></ul>", unsafe_allow_html=True)
			st.write("")
			st.sidebar.text("")
			st.sidebar.text("")
			st.sidebar.text("")
			st.sidebar.markdown("<p style ='color: black;'>Created by:</p>", unsafe_allow_html=True)
			st.sidebar.markdown("<p style='color: black;margin-left: 20px;'>Mahmoud Sorour Ragab</p>", unsafe_allow_html=True)

			user_input = st.text_input("Enter URL:")
			a = function_features.get_features(user_input)
					
			with open('scaler.pkl', 'rb') as f:
				
					scaler = pickle.load(f)
					
			df= scaler.transform(a)
			with open('best_model_pkl', 'rb') as pickle_file:
					model_pkl = pickle.load(pickle_file)
			t = Timer()
			t.start()
			predicted = model_pkl.predict(df)
			s = t.stop()
			st.sidebar.markdown("<p style ='color: black;'>Prediction :</p>", unsafe_allow_html=True)
			st.sidebar.text(str(s))
				
			center_button_container = st.container()
			with center_button_container:
				col1, col2, col3 = st.columns([4, 1, 3.5])
				submit = col2.button('Predict')

			# st.write("")
			# submit = st.button('Predict')
			if (user_input==""):
				st.write("")
				st.write("")
				st.markdown("<p style='color: black;margin-left: 368px;'>Please input a valid URL</p>", unsafe_allow_html=True)
			if submit and user_input!="":
				if(predicted == 0):
					st.header("Type of URL : is Benign")
				if(predicted == 1):
					st.header("Type of URL : is Malicious")
				if (predicted == 0):
					image = Image.open("benign.png")
					st.sidebar.image(image)
				else:
					image = Image.open("malicious.jpeg")
					st.sidebar.image(image)


		


			
		