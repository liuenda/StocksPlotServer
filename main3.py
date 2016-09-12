# -*- coding: utf-8 -*-
# %matplotlib inline
import pandas as pd
import numpy as np
import ffn
import bt
import ffn
import datetime
from dateutil import parser
from io import BytesIO
import matplotlib.pyplot as plt, mpld3
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)
input_filename="input.csv"
period=100 # period of display in days

# """
# return a png figure
# """
# def plot1():
# 	fig = Figure()
# 	axis = fig.add_subplot(1, 1, 1)

# 	xs = range(100)
# 	ys = [random.randint(1, 50) for x in xs]

# 	axis.plot(xs, ys)
# 	canvas = FigureCanvas(fig)
# 	output = StringIO.StringIO()
# 	canvas.print_png(output)
# 	response = make_response(output.getvalue())
# 	response.mimetype = 'image/png'
# 	return response

"""
save a png figure
"""
def plot2(s):
	# Date parsing and calculation
	date_string=s[0]
	dt = parser.parse(date_string)
	dt_min = dt - datetime.timedelta(period)
	dt_max = dt + datetime.timedelta(period)
	df_min_string = dt_min.date().isoformat()
	df_max_string = dt_max.date().isoformat()
	stocks=s[1]
	print "DEBUG s:"
	print s
	# retrieve stocks 


	# download price data from Yahoo! Finance. By default,
	# the Adj. Close will be used.
	prices = ffn.get(stocks, start=df_min_string, end=df_max_string)
	# let's compare the relative performance of each stock
	# we will rebase here to get a common starting point for both securities
	
	ax = prices.rebase().plot(figsize=(10,5))
	# save the figure
	fig = ax.get_figure()
	fig.tight_layout()	

	# fig.savefig(date_string+stocks+'.svg',format='svg')
	# fig.savefig(date_string+stocks+'.png',format='png')

	print "save the a picture finished!"
	
	# fig.show()
	
	return fig

def convert2svg(fig):
	# save as svg string
	figfile = BytesIO()
	fig.savefig(figfile, format='svg')
	# figdata_svg = figfile.getvalue()
	figdata_svg = '<svg' + figfile.getvalue().split('<svg')[1]
	figdata_svg = unicode(figdata_svg, 'utf-8')
	return figdata_svg

	

def convert2mpld3(fig):
	html_text = mpld3.fig_to_html(fig)

def parse_xml(html):
	soup = BeautifulSoup(html)
	soup.head.string
	soup.body.strin



# @app.route("/"+figue_name)
# def display(figue_name):
# 	plot2()
# 	return figure_path

@app.route("/")
def index():
	return render_template("HomePage.html", df=df, fig=fig, figdata_svg=figdata_svg)

@app.route("/<int:index>",methods=['GET'])
def retrieve_figure(index):
	print "the index list is ", index
	if index not in range(fig.size):
		abort(404)
		flash()
	return figdata_svg[index]

if __name__ == "__main__":

	df = pd.read_csv(input_filename, names=['data','stocks'])
	fig= df.apply(plot2,axis=1)
	figdata_svg = fig.apply(convert2svg)

	
	# Conver matplotlib figure to mpld3 html figure
	# html_text = mpld3.fig_to_html(fig[0])
	# s_html = fig.apply(mpld3.fig_to_html)
	# s_html_body = s_html.apply(parse_xml)

	app.run(debug = True,host= '0.0.0.0')