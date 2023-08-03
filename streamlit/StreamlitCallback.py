import streamlit as st
from tensorflow.keras.callbacks import Callback

class StreamlitCallback(Callback):
    def on_train_begin(self, logs=None):
        self.text_area = st.empty()  
        self.training_logs = []
        self.text_area.markdown('Starting training')

    def on_epoch_end(self, epoch, logs=None):
        log_line = f'Epoch {epoch}, loss: {logs["loss"]:.4f}, mean_squared_error: {logs["mean_squared_error"]:.4f}, val_loss: {logs["val_loss"]:.4f}, val_mean_squared_error: {logs["val_mean_squared_error"]:.4f}'
        self.training_logs.append(log_line)
        self.text_area.markdown('<br>'.join(self.training_logs), unsafe_allow_html=True)
