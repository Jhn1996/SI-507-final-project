# Covid-19 New York Times Data Insights

## Instructions
A Newsapi key is needed to run the program, you can register and retrieve the key at https://newsapi.org/.

Copy the API key to a python file named secrets.py under the current directory with the following format:
	NEWSAPI_KEY = 'your api key'

## To run the program:
1.Clone the GitHub repository to your local computer
2.Create secrets.py with the above instruction, and place it in the same directory.
3.Open the directory folder with your python idle (Atom, vscode, etc)
4.Select “covid_insight_app.py”, and run the file.
5.Navigate to “http://127.0.0.1:5000/” to see the visual
6.The date displayed  will be auto-updated based on the latest date from the original data source
7.Click on the 5 top news titles will take you to an external page with the news article, to allow the user to learn about the  top articles about Covid 19.
8.View the latest visualization about the “Overall Cases and Death Number Across the States in the United States” hover over each bar graph to see exact case and death numbers(accumulated) up to date.
10.Type in the state name in the input field and click search, the page will direct to a new page, where users can learn about county cases and death data with the state he or she inputted.
11.View the graph and chart, go back and repeat to search for more state.

## Required Python packages for your project to work:
Users need to pip install the following packages
urllib, requests, flask, sqlite3, plotly
