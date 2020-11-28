# TimeString

Interactive time series visualization using Bokeh and D3.js. Check out a live demo [here](https://hnagib.com/ts-cluster). The applet can be useful for finding patterns in large sets of timeseries data. 

Features: 
- Runs linear regression for all variables in the selected segment
- Sort variables by trend over selected segment, number of upper/lower control limit violations
- Calculate Dynamic Time Wrapping distance for selected variable segment against all other variables
- Compute agglomerative heirarchical clustering for selected segments and display results in a d3.js dendogram

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
