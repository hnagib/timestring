# TimeString

Interactive time series visualization using Bokeh and D3.js. Check out a live demo using S&P100 stock price data [here](https://hnagib.com/ts-cluster). This tool can help you quickly identify patterns in large sets of time series data.   

### Features: 
- Runs linear regression for all variables in the selected segment
- Sort variables by trend over selected segment, number of upper/lower control limit violations
- Calculate Dynamic Time Wrapping or Eucledian distance for selected variable segment against all other variables
- Compute agglomerative heirarchical clustering for selected segments and display results in an interactive d3.js dendogram

:open_file_folder: Repo Organization
--------------------------------

    ├── src                
    │   ├── cluster.js              <-- Heirarchical clustering  
    │   ├── dtw.js                  <-- Calculating dynamitc time wrapping distance
    │   ├── htmltext.py             <-- JS and HTML to be embed in bokeh dashboard
    │   └── ts-cluster.html         <-- Dashboard 
    │
    ├── notebooks          
    │   ├── hn-create-dash.ipynb     <-- Create dashboard        
    │   └── ...            
    │
    ├── Makefile           <- Makefile with commands to automate installation of python environment
    ├── requirements.txt   <- List of python packages required     
    ├── README.md
    └── .gitignore         
