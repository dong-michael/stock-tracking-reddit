import matplotlib.pyplot as plt 
import psycopg2
import psycopg2.extras



def visualize_data (stocks):
    figure = plt.figure(figsize = (20, 8))
    axes = figure.add_subplot(1 ,1, 1)

    axes.barh (
        [stock[2] for stock in stocks[:25]],
        [stock[0] for stock in stocks[:25]]
    )

    axes.set_xlabel('Popularity (# of mentions)')
    axes.set_ylabel('Stock Ticker')
    axes.set_title('Top 25 Hottest Stocks on WSB')

    return figure