import panel as pn
import pandas as pd
pn.extension()



#Widgets
##text box for ticker
ticker = pn.widgets.TextInput(name="Ticker", value="AAPL", width=150)

##date picker
start_date = pn.widgets.DatePicker(name="Start Date", value=pd.to_datetime("2000-01-01"))
end_date = pn.widgets.DatePicker(name="End Date", value=pd.to_datetime("2025-01-01"))

##slider for monthly contrib
monthly_contrib = pn.widgets.IntSlider(name="Monthly Contribution ($)", start=50, end=1000, step=50, value=150)

##box checker for strategy selection
strategy_selector = pn.widgets.CheckBoxGroup(name="Strategies", 
                                             options=["DCA",  
                                                      "Double Down DCA", 
                                                       "Lump Sum", 
                                                       "Simple Moving Average DCA", 
                                                       "Value Averaging"],
                                                       value=["DCA"],
                                                       inline=False)

##dropdown for var plotting
plot_var = pn.widgets.Select(name="Variable to plot",
                             options=["portf_value", "invested_total", "shares_total", "profit_loss"],
                             value="portf_value")

##run button
run_button = pn.widgets.Button(name="Run Simulation", button_type="primary")




#Output
##plot
plot_pane = pn.pane.Markdown("*(Plot here after pressing run)*")

##metrics comparison table
metrics_pane = pn.pane.Markdown("*(Metrics table here after run)*")



#Layout
template = pn.template.FastListTemplate(title = "Investment Strategy Comparison Tool",
    sidebar=[ticker, 
             start_date, 
             end_date, 
             monthly_contrib, 
             pn.pane.Markdown("### Strategies"), 
             strategy_selector, 
             pn.pane.Markdown("### Plot Settings"), 
             plot_var, 
             run_button],

    main=[pn.pane.Markdown("## Strategy Plot"),
          plot_pane,
          pn.pane.Markdown("## Key Metrics Comparison"),
          metrics_pane])

template.servable()



def run_simulation(simulation):
    """Run the simulation with the specified parameters from the "Run Simulation" button"""

    selected_ticker = ticker.value
    selected_strategies = strategy_selector.value
    selected_var = plot_var.value
    start = start_date.value
    end = end_date.value
    monthly_c = monthly_contrib.value

    plot_pane.object = (f'###plot\n'
                        f'Ticker: **{selected_ticker}**\n')
    
    metrics_pane.object = "*(metrics to be computed)*"


#connecting button with run_simulation
run_button.on_click(run_simulation)