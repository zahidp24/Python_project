import matplotlib.pyplot as plt

def plot_profit_loss(*dfs, labels=None):
    """Used to plot plofit_loss of different strategies in one graph for comparison"""

    plt.figure(figsize=(12,6))

    if labels is None: #if one forgets to specify the label
        labels = [f"Strategy {i+1}" for i in range(len(dfs))]

    for  i, df in enumerate(dfs):
        plt.plot(df.index, df["profit_loss"], label = labels[i])

    plt.title("Profit/Loss Comparison")
    plt.xlabel("Date")
    plt.ylabel("Profit/Loss ($ million)")
    plt.grid(False)
    plt.legend()
    plt.show()


def plot_portf_value(*dfs, labels=None):
    """Used to plot portf_value of different strategies in one graph for comparison"""

    plt.figure(figsize=(12,6))

    if labels is None: #if one forgets to specify the label
        labels = [f"Strategy {i+1}" for i in range(len(dfs))]

    for i, df in enumerate(dfs):
        plt.plot(df.index, df["portf_value"], label=labels[i])

    plt.title("Portfolio Value Comparison")
    plt.xlabel("Date")
    plt.ylabel("Profit/Loss ($10s million)")
    plt.grid(False)
    plt.legend()
    plt.show()  


def plot_shares_total(*dfs, labels=None):
    """Used to plot shares_total of different strategies in one graph for comparison"""

    plt.figure(figsize=(12,6))

    if labels is None: #if one forgets to specify the label
        labels = [f"Strategy {i+1}" for i in range(len(dfs))]

    for  i, df in enumerate(dfs):
        plt.plot(df.index, df["shares_total"], label = labels[i])

    plt.title("Accumulated shares Comparison")
    plt.xlabel("Date")
    plt.ylabel("Accumulated shares")
    plt.grid(False)
    plt.legend()
    plt.show()



def plot_monthly_investment(*dfs, labels=None):
    """Used to plot monthly_investment of different strategies in one graph for comparison"""

    plt.figure(figsize=(12,3))

    if labels is None: #if one forgets to specify the label
        labels = [f"Strategy {i+1}" for i in range(len(dfs))]

    for  i, df in enumerate(dfs):
        invested_monthly = df["invested_total"].diff()
        plt.plot(df.index, invested_monthly, label = labels[i])

    plt.title("Invested Amount per month over time")
    plt.xlabel("Date")
    plt.ylabel("Invested Amount per month")
    plt.grid(False)
    plt.legend()
    plt.show()



def plot_invested_total(*dfs, labels=None):
    """Used to plot cumulative invested_total of different strategies in one graph for comparison"""

    plt.figure(figsize=(12,3))

    if labels is None: #if one forgets to specify the label
        labels = [f"Strategy {i+1}" for i in range(len(dfs))]

    for  i, df in enumerate(dfs):
        plt.plot(df.index, df["invested_total"], label = labels[i])

    plt.title("Cumulative Invested Amount  over time")
    plt.xlabel("Date")
    plt.ylabel("Invested Total ($)")
    plt.grid(False)
    plt.legend()
    plt.show()