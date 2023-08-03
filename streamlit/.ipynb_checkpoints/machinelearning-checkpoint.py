# importing libraries
import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
import hvplot.pandas
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import time
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.metrics import MeanSquaredError
from pandas.tseries.offsets import DateOffset
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from bokeh.models.formatters import NumeralTickFormatter
import holoviews as hv
hv.extension('bokeh', logo=False)
from KerasCustomCallback import KerasCustomCallback
from StreamlitCallback import StreamlitCallback

def render_page():
    all_values = pd.read_csv(Path("../Resources/all_values_superset.csv"))
    all_values['date'] = pd.to_datetime(all_values['date'], format='%Y-%m')
    all_values.set_index('date', inplace=True)
    all_values.drop(columns=['All-items 8', 'All-items excluding food', 'All-items excluding food and energy'], inplace=True)
    all_values.dtypes

    #st.write(all_values.dtypes)

    scaler_all = StandardScaler()
    all_scaler = scaler_all.fit(all_values)
    all_values_scaled = all_scaler.transform(all_values)

    all_values_scaled_df = pd.DataFrame(all_values_scaled, columns=all_values.columns, index=all_values.index)
    all_values_scaled_df.head()

    st.write(all_values_scaled_df)

    targets = [col for col in all_values_scaled_df.columns.tolist() if col.find('Benchmark') > 0]

    y = all_values_scaled_df[targets]
    X = all_values_scaled_df.drop(columns = targets)
    y.shape
    st.write(y.shape)

    y.head()

    X.head()

    all_values_plot = all_values_scaled_df.hvplot(
        height=800,
        width=1600
    )
    st.write(hv.render(all_values_plot, backend='bokeh'))

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    X_train
    X_test.sort_index(ascending=True, inplace=True)
    y_train
    y_test.sort_index(ascending=True, inplace=True)
    y_test_size = y_test.shape[0]
    y_test_size

    # Neural network parameters
    n_input_feats = len(X.columns)

    n_outputs = 161

    hidden_nodes_layer1 = 128
    hidden_nodes_layer2 = 512
    hidden_nodes_layer3 = 1024
    # hidden_nodes_layer4 = 4

    parameters = f"""
    Neural Network Parameters:
    --------------------------
    Input Features: {n_input_feats}
    Layers:         3
    Layer1 Nodes:   {hidden_nodes_layer1}
    Layer2 Nodes:   {hidden_nodes_layer2}
    Layer3 Nodes:   {hidden_nodes_layer3}
    Output Nodes:   {n_outputs}
    """
    print(parameters)
    st.write(f"Neural Network Parameters:")
    st.write(f"--------------------------")
    st.write(f"Input Features: {n_input_feats}")
    st.write(f"Layers:         3")
    st.write(f"Layer1 Nodes:   {hidden_nodes_layer1}")
    st.write(f"Layer2 Nodes:   {hidden_nodes_layer2}")
    st.write(f"Layer3 Nodes:   {hidden_nodes_layer3}")
    st.write(f"Output Nodes:   {n_outputs}")

    # define model
    nn = Sequential()

    # Add the first hidden layer
    nn.add(Dense(
        units=hidden_nodes_layer1,
        input_dim = n_input_feats,
        activation='relu',
        name='hidden1'
    ))

    # Add the second hidden layer
    nn.add(Dense(
        units=hidden_nodes_layer2,
        activation='relu',
        name='hidden2'
    ))

    # Add the third hidden layer
    nn.add(Dense(
        units=hidden_nodes_layer3,
        activation='relu',
        name='hidden3'
    ))

    # Add output
    nn.add(Dense(
        n_outputs,
        activation='linear',
        name='output'
    ))

    # Display the Sequential model summary
    #st.write(nn.summary())
    nn.summary(print_fn=lambda x: st.text(x))

    # Compile the Sequential model
    nn.compile(loss='mean_squared_error', optimizer='adam', metrics=[MeanSquaredError()])

    st.write("X_train")
    st.write(X_train)

    # Fit the model using 100 epochs and the training data
    model = nn.fit(
        X_train,
        y_train,
        batch_size=10,
        validation_split=0.2,
        epochs=100,
        callbacks=[StreamlitCallback()]
    )

    # R2 score for training
    train_pred = nn.predict(X_train)
    #training_r2 = r2_score(y_train.values, train_pred)
    # model_loss, model_accuracy = nn.evaluate(X_test, y_test)
    #training_r2

    # Create a DataFrame with the history dictionary
    model_df = pd.DataFrame(model.history, index=range(1, len(model.history["loss"]) + 1))

    # Plot the loss
    val_loss_plot = model_df.hvplot(
        y="val_loss",
    )
    st.write(hv.render(val_loss_plot, backend='bokeh'))

    # Plot the accuracy
    mean_squared_error_plot = model_df.hvplot(y="mean_squared_error")

    st.write(hv.render(mean_squared_error_plot, backend='bokeh'))

    both_plot = model_df[['val_loss', 'mean_squared_error']].hvplot(
        height=800,
        width=2000
    )
    st.write(hv.render(both_plot, backend='bokeh'))

    predictions = nn.predict(X_test)
    # predictions = nn.predict(X_test.sort_index(ascending=True))

    # R2 score from test
    #test_r2 = r2_score(y_test.values, predictions)
    # test_r2 = r2_score(y_test.sort_index(ascending=True).values, predictions)
    #test_r2

    all_values_pred = nn.predict(X)
    all_values_pred.shape

    all_feats_pred = nn.predict(X)
    all_feats_pred_df = pd.DataFrame(all_feats_pred, columns=y.columns, index=X.index)
    all_preds_feats_scaled_df = pd.concat([all_feats_pred_df, X], axis=1)
    all_preds_feats_descaled = all_scaler.inverse_transform(all_preds_feats_scaled_df)
    all_preds_feats_descaled_df = pd.DataFrame(all_preds_feats_descaled, columns=all_preds_feats_scaled_df.columns, index=all_preds_feats_scaled_df.index)
    all_preds_descaled_df = all_preds_feats_descaled_df[targets]
    all_preds_descaled_df.columns = ['PRED_'+col for col in all_preds_descaled_df.columns]
    all_preds_descaled_df
    # all_preds_feats_descaled_df
    # all_pred_real = all_values_scaled_df.copy()
    # all_pred_real['Composite'] = all_values_pred
    # all_values_descaled = all_scaler.inverse_transform(all_pred_real)
    # all_values_descaled_df = pd.DataFrame(all_values_descaled, columns=all_values_scaled_df.columns, index=all_values_scaled_df.index)
    # all_values_descaled_df
    # all_values_descaled_df['Predicted'] = all_values_descaled_df['Composite']
    # all_values_descaled_df['Composite'] = all_values['Composite']
    # all_values_descaled_df

    all_targets_pred_compare_df = pd.concat([all_preds_descaled_df, all_values[targets]], axis=1)
    all_targets_pred_compare_df.hvplot(
        xlabel='Date', 
        ylabel='Price', 
        title='Actual and Predicted Index',
        height=800,
        width=1600,
        legend=False    
    ).opts(
        yformatter=NumeralTickFormatter(format="0,0")
    )

    nn_json = nn.to_json()

    #file_path = ("../Models/model3.json")
    #with open(file_path, "w") as json_file:
    #    json_file.write(nn_json)

    #file_path = "../Models/model3.h5"
    #nn.save_weights(file_path)

    def mean_absolute_percentage_error(y_true, y_pred): 
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    def weighted_absolute_percentage_error(y_true, y_pred):
        return 100 / len(y_true) * np.sum(np.abs((y_true - y_pred) / y_true))

    def weighted_mean_absolute_percentage_error(y_true, y_pred):
        return 100 / sum(y_true) * np.sum(np.abs(y_true - y_pred))

    # Generate predictions
    y_pred = nn.predict(X_test)

    # Calculate R-Squared
    #r2 = r2_score(y_test, y_pred)

    # Calculate Mean Absolute Error
    mae = mean_absolute_error(y_test, y_pred)

    # Calculate Mean Absolute Percentage Error
    mape = mean_absolute_percentage_error(y_test, y_pred)

    # Calculate Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)

    # Calculate Root Mean Squared Error
    rmse = np.sqrt(mse)

    #print(f"R-Squared: {r2}")
    print(f"Mean Absolute Error: {mae}")
    print(f"Mean Absolute Percentage Error: {mape}")
    print(f"Mean Squared Error: {mse}")
    print(f"Root Mean Squared Error: {rmse}")

    #all_preds_descaled_df.to_csv('Resources/total_chart_regional_save.csv', index=True)