import panel as pn
import pandas as pd
import datetime as dt
pn.extension()
import hvplot.pandas
import holoviews as hv
from bokeh.models import HoverTool
from bokeh.models import NumeralTickFormatter

from dca_simulator.data_loader import load_price_data
from dca_simulator.strategies import (dca_standard, dca_DD, lump_sum, dca_sma_mom, dca_sma_mean_rev, value_averaging)
from dca_simulator.metrics import compute_KeyMetrics





###Widgets###
##text box for ticker
ticker = pn.widgets.TextInput(name="Ticker", value="AAPL", width=150)

##date picker
start_date = pn.widgets.DatePicker(name="Start Date", value=pd.to_datetime("2010-01-01"))
end_date = pn.widgets.DatePicker(name="End Date", value=dt.date.today())

##sliders for strategy parameters
monthly_contrib = pn.widgets.IntSlider(name="Monthly Contribution ($)", start=50, end=1000, step=50, value=150)
growth_slider = pn.widgets.FloatSlider(name="Desired Monthly Growth rate (SMA)", start=0.001, end=0.01, step=0.001, value=0.006, format="0.000")
sma_period_slider = pn.widgets.IntSlider(name="SMA period", start=10, end=300, step=10, value=90)
DD_treshold_slider = pn.widgets.FloatSlider(name="Double Down Treshold", start=0.05, end=0.6, step=0.05, value=0.15)


##box checker for strategy selection
strategy_selector = pn.widgets.CheckBoxGroup(name="Strategies", 
                                             options=["DCA",  
                                                      "Double Down DCA", 
                                                       "Lump Sum", 
                                                       "Simple Moving Average DCA - Momentum",
                                                       "Simple Moving Average DCA - Mean Reversion",
                                                       "Value Averaging"],
                                                       value=["DCA"],
                                                       inline=False)


##plot variable options
plot_var_options = {
    "Portfolio Value ($)": "portf_value",
    "Total Invested ($)": "invested_total",
    "Accumulated Shares": "shares_total",
    "Profit/Loss ($)": "profit_loss"
}

##dropdown for var plotting
plot_var = pn.widgets.Select(name="Variable to plot",
                             options=list(plot_var_options.keys()),
                             value="Portfolio Value ($)")

##run button
run_button = pn.widgets.Button(name="Run Simulation", button_type="primary")


##labels (used to display several variables such as portf_total, invested_total, etc.)
var_labels = {
    "portf_value": "Portfolio Value ($)",
    "invested_total": "Total Invested ($)",
    "shares_total": "Accumulated Shares",
    "profit_loss": "Profit/Loss ($)"}




###Output###
##preview
preview_pane = pn.pane.HoloViews(None, sizing_mode="stretch_width", height=350)

##plot
plot_pane = pn.pane.HoloViews(None, sizing_mode="stretch_width", height = 350)

##metrics comparison table
metrics_pane = pn.pane.DataFrame(None, sizing_mode="stretch_width")


#Layout
template = pn.template.FastListTemplate(title = "Retail Investment Strategy Backtester",
    sidebar=[ticker, 
             start_date, 
             end_date, 
             monthly_contrib, 
             growth_slider,
             sma_period_slider,
             DD_treshold_slider,
             pn.pane.Markdown("### Strategies"), 
             strategy_selector, 
             pn.pane.Markdown("### Plot Settings"), 
             plot_var, 
             run_button],

    main=[pn.pane.Markdown("## Data Preview"),
          preview_pane,
          pn.pane.Markdown("## Strategy Plot"),
          plot_pane,
          pn.pane.Markdown("## Key Metrics"),
          metrics_pane])

template.servable()



###Simulation func###
def run_simulation(simulation):
    """Run the simulation with the specified parameters from the "Run Simulation" button"""

    selected_ticker = ticker.value
    selected_strategies = strategy_selector.value
    selected_var = plot_var_options[plot_var.value]
    start = start_date.value
    end = end_date.value
    monthly_c = monthly_contrib.value
    growth = growth_slider.value
    sma_p = sma_period_slider.value
    dd_tresh = DD_treshold_slider.value

    ##Data loading
    try:    
        df = load_price_data(selected_ticker, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))

        if df is None or df.empty:
            raise ValueError(f"No data found for ticker '{selected_ticker}'.")
        
        preview_pane.object = df.hvplot.line(y="Close", title=f"{selected_ticker} Price History", responsive=True)
    

    except Exception as e:
        preview_pane.object = pn.pane.Markdown(f"**Error loading the data:** {str(e)}")
        plot_pane.object = None
        metrics_pane.object = None
        return


    ##Strategies
    results = {}

    for strat in selected_strategies:
        if strat == "DCA":
            results["DCA"] = dca_standard(df, monthly_c)
        
        elif strat == "Double Down DCA":
            results["Double Down DCA"] = dca_DD(df, monthly_c, dd_tresh)

        elif strat == "Lump Sum":
            results["Lump Sum"] = lump_sum(df, monthly_c)

        elif strat == "Simple Moving Average DCA - Momentum":
            results["SMA Momentum"] = dca_sma_mom(df, monthly_c, sma_p)
        
        elif strat == "Simple Moving Average DCA - Mean Reversion":
            results["SMA Mean Reversion"] = dca_sma_mean_rev(df, monthly_c, sma_p)
        
        elif strat == "Value Averaging":
            results["Value Averaging"] = value_averaging(df, growth, monthly_c)




    ##Plotting
    plots = []



    def format_axis(plot, element):
        """Format y-axis to show $ sign and commas for money variables """
        fmt="$0,0" if selected_var in ["portf_value", "invested_total", "profit_loss"] else "0,0"
        plot.state.yaxis.formatter = NumeralTickFormatter(format=fmt)



    for name, df_result in results.items():
        curve = df_result.hvplot(y=selected_var, 
                                 ylabel=var_labels[selected_var], 
                                 label=name, #legend label
                                 title=f"{var_labels[selected_var]} over Time",
                                 height=350, 
                                 responsive=True).opts(hooks=[format_axis]) #format y-axis to financial notation
        plots.append(curve)

    interact_plot = plots[0]
    for curve in plots[1:]:
        interact_plot *= curve #add the curves on top of each other

    plot_pane.object = interact_plot



    ##Key Metrics table
    metrics_list = []

    for name, df_result in results.items():
        try:
            metrics = compute_KeyMetrics(df_result)
            metrics["Strategy"] = name
            metrics_list.append(metrics)
        except Exception as e:
            print(f'Error computing metrics for {name}: {e}')

    
    metrics_df = pd.DataFrame(metrics_list).set_index("Strategy")
    metrics_pane.object = metrics_df



##connecting button with run_simulation
run_button.on_click(run_simulation)
