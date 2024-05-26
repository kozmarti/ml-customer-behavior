import matplotlib.pyplot as plt
import mpld3

from services.constants import COLORS


def get_histograms(data, columns):
    plot_list_html = []
    colors = COLORS[:len(columns)]
    for index, column in enumerate(columns):
        fig = plt.figure()
        data[column].plot(kind='hist', title=column, xlabel="Amount spent ($)",
                          ylabel="Customer (person)",
                          color=colors[index], lw=0)
        plot_list_html.append(mpld3.fig_to_html(fig))
    return plot_list_html


def get_pie_charts(data, columns):
    chart_list_html = []
    for column in columns:
        fig = plt.figure()
        data[column].value_counts().plot.pie(title=column, startangle=40,
                                             autopct='%1.1f%%', figsize=(5, 5),
                                             shadow=False,
                                             legend=True,
                                             ylabel='',
                                             labeldistance=None,
                                             fontsize=2, colors=COLORS)
        chart_list_html.append(mpld3.fig_to_html(fig))
    return chart_list_html