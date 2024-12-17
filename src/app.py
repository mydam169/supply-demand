import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
# import webbrowser
# import threading


# Initialize the Dash app
app = dash.Dash(__name__)
# add server for web deployment
server = app.server

# Layout of the app
app.layout = html.Div([
    html.H1("Supply and Demand Interactive Tool"),

    dcc.Graph(id='supply-demand-graph'),
    
    html.Label("Adjust Demand Curve Intercept (a):"),
    dcc.Slider(id='demand-intercept-slider', min=0, max=100, value=80, marks={i: str(i) for i in range(0, 101, 10)}),
    
    html.Label("Adjust Demand Curve Slope (b):"),
    dcc.Slider(id='demand-slope-slider', min=-5, max=-0.1, value=-0.5, step=0.1, marks={i: str(i) for i in range(-5, 1, 1)}),
    
    html.Label("Adjust Supply Curve Intercept (c):"),
    dcc.Slider(id='supply-intercept-slider', min=0, max=100, value=10, marks={i: str(i) for i in range(0, 101, 10)}),
    
    html.Label("Adjust Supply Curve Slope (d):"),
    dcc.Slider(id='supply-slope-slider', min=0.1, max=5, value=0.5, step=0.1, marks={i: str(i) for i in range(1, 6, 1)}),

])

# Callback to update the graph
@app.callback(
    Output('supply-demand-graph', 'figure'),
    Input('demand-intercept-slider', 'value'),
    Input('demand-slope-slider', 'value'),
    Input('supply-intercept-slider', 'value'),
    Input('supply-slope-slider', 'value')
)
def update_graph(demand_intercept, demand_slope, supply_intercept, supply_slope):
    # Generate data for demand and supply curves
    quantity = np.linspace(0, 100, 100)
    demand = demand_intercept + demand_slope * quantity  # Demand curve: P = a + bQ
    supply = supply_intercept + supply_slope * quantity  # Supply curve: P = c + dQ

    # Calculate equilibrium price and quantity
    # Set demand equal to supply: a + bQ = c + dQ
    # Rearranging gives: Q = (c - a) / (b - d)
    equilibrium_quantity = (supply_intercept - demand_intercept) / (demand_slope - supply_slope)
    equilibrium_price = demand_intercept + demand_slope * equilibrium_quantity

    # Calculate consumer surplus and producer surplus
    consumer_surplus = 0.5 * (demand_intercept - equilibrium_price) * equilibrium_quantity
    producer_surplus = 0.5 * (equilibrium_price - supply_intercept) * equilibrium_quantity

    # Create the figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=quantity, y=demand, mode='lines', name='Demand Curve', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=quantity, y=supply, mode='lines', name='Supply Curve', line=dict(color='red')))
    
    # Add equilibrium point
    fig.add_trace(go.Scatter(x=[equilibrium_quantity], y=[equilibrium_price], mode='markers', name='Equilibrium', marker=dict(color='green', size=15)))

    # Shade the area representing consumer surplus
    fig.add_trace(go.Scatter(
        x=[0, equilibrium_quantity, 0],
        y=[demand_intercept, equilibrium_price, equilibrium_price],
        fill='toself',
        fillcolor='rgba(0, 0, 255, 0.2)',  # Light blue color for consumer surplus
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Consumer Surplus'
    ))

    # Shade the area representing producer surplus
    fig.add_trace(go.Scatter(
        x=[0, equilibrium_quantity, 0],
        y=[equilibrium_price, equilibrium_price, supply_intercept],
        fill='toself',
        fillcolor='rgba(255, 0, 0, 0.2)',  # Light red color for producer surplus
        line=dict(color='rgba(255, 255, 255, 0)'),
        name='Producer Surplus'
    ))

    # Update layout
    fig.update_layout(title='Supply and Demand Curves', 
                      xaxis_title='Quantity', 
                      yaxis_title='Price', yaxis_range=[0, 100])
    
    return fig

# Debugging
# if __name__ == '__main__':
#     app.run_server(debug=True)

# click "http://127.0.0.1:8050" to view app on local machine

# for production
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=False)