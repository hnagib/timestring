from bokeh.models.widgets import Div

div_space = '<div style="width: {width}px; height: {height}px;"></div>'

def space(width, height=0):
    return Div(text=div_space.format(width=width, height=height))


template = """
  <!DOCTYPE html>
  <html lang="en">
  {% block head %}
      
  <head>
      {% block inner_head %}
      <meta charset="utf-8">
  

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <!-- Social icon CSS -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <!-- Load d3.js & d3 tip-->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/d3-tip/0.7.1/d3-tip.min.js"></script>
        <!-- Stats library -->
        <script src="https://cdn.jsdelivr.net/npm/jstat@latest/dist/jstat.min.js"></script>
        
        <!-- local JS modules -->
        <script src="dtw.js"></script>
        <script src="cluster.js"></script>
        <script src="plot_cluster.js"></script>


        <link rel="stylesheet" href="style.css">

        <!-- Navigation Bar -->
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav mr-auto">
              <li class="nav-item active">
                <a class="nav-link" style=" font-size:16px font-family:helvetica; color:grey;" href="https://www.hnagib.com">Home<span class="sr-only">(current)</span></a>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" style=" font-size:16px font-family:helvetica; color:grey;" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Projects
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                  <a class="dropdown-item" style=" font-size:16px font-family:helvetica; color:grey;" href="https://www.hnagib.com/ts-cluster">TimeString</a>
                </div>
              </li>
            </ul>
          </div>
        </nav>


  <body>
      
      
    </body>

      <title>{% block title %}{{ title | e if title else "Bokeh Plot" }}{% endblock %}</title>
      {% block preamble %}{% endblock %}
      {% block resources %}
          {% block css_resources %}
          {{ bokeh_css | indent(8) if bokeh_css }}
          {% endblock %}
          {% block js_resources %}
          {{ bokeh_js | indent(8) if bokeh_js }}
          {% endblock %}
      {% endblock %}
      {% block postamble %}{% endblock %}
      {% endblock %}
  </head>
  {% endblock %}
  {% block body %}
  <body>
  <div style="font-size:12px; font-family:helvetica; color:grey; margin-left: 40px; width: 900px; float: left;">
      {% block inner_body %}
      {% block contents %}
          {% for doc in docs %}
          {{ embed(doc) if doc.elementid }}
          {% for root in doc.roots %}
              {{ embed(root) | indent(10) }}
          {% endfor %}
          {% endfor %}
      {% endblock %}
      {{ plot_script | indent(8) }}
      {% endblock %}
  </div>
  </body>
  {% endblock %}
  </html>
"""


plot_cluster = """
  if (select_dist.value == "dtw"){var clust = hcluster(selected_data["y"],dtwDist)}
  else if (select_dist.value == "euclid"){var clust = hcluster(selected_data["y"],euclid)}

  var labels = selected_data["variable"]
  deepIterator(clust, labels)
  
  plot_cluster(clust, var_meta, select)
"""

sum_calc = """
            const inds = cds_tsplot.selected.indices;
            const data = cds_tsplot.data;
            var m = 0
            var dist = 0
            var y = []
            var y_norm = []
            var x = []
            
            var summary_data = {{
                "variable":[],
                "group":[], 
                "slope":[],
                "usl":[],
                "lsl":[],
                "dist":[]
            }}
            
            var selected_data = {{
                "variable":[],
                "y":[]
            }}
            
            // In sufficient data selected
            if (inds.length <= 1) {{ {alert} return;}}
            
            else {{
                for (var key in var_meta) {{

                    x = []
                    y = []
                    var y_usl_breach = []
                    var y_lsl_breach = []
                    
                    var y_comp = []

                    for (var i = 0; i < inds.length; i++) {{
                        y.push(data[key][inds[i]])
                        
                        y_comp.push(data[select.value][inds[i]])
                        
                        y_usl_breach.push(data[key][inds[i]] >= data[key+"_usl"][inds[i]])
                        y_lsl_breach.push(data[key][inds[i]] <= data[key+"_lsl"][inds[i]])
                        
                        x.push([1, inds[i]])
                    }} 
                    
                    
                    m = jStat.models.ols(y,x).coef[1];     
                    
                    summary_data["variable"].push(key)
                    summary_data["group"].push(var_meta[key]["category"])
                    summary_data["slope"].push(parseFloat((m*inds.length).toFixed(3)))
                    summary_data["usl"].push(y_usl_breach.filter((value) => value).length)
                    summary_data["lsl"].push(y_lsl_breach.filter((value) => value).length)
                    summary_data["dist"].push(parseFloat(dist.toFixed(3)))
                    
                    selected_data["variable"].push(key)
                    selected_data["y"].push(y)
                                        
                }}
            
            }}
            cds_selection_summary_data.data["variable"] = summary_data["variable"]
            cds_selection_summary_data.data["group"] = summary_data["group"]
            cds_selection_summary_data.data["slope"] = summary_data["slope"]
            cds_selection_summary_data.data["usl"] = summary_data["usl"]
            cds_selection_summary_data.data["lsl"] = summary_data["lsl"]
            
            cds_tsplot.change.emit();
            cds_selection_summary_data.change.emit();
"""


dist_calc = """
            if (cds_tsplot.selected.indices.length <= 1) {alert("Select a segment of the time series using the box select tool"); return;}

            const inds = cds_tsplot.selected.indices;
            const data = cds_tsplot.data;
            var dist = 0
            var y = []
            var y_norm = []
            
            var summary_data = {
                "variable":[], 
                "dist":[]
            }
            
            var selected_data = {
                "variable":[],
                "y":[]
            }
            
            // In sufficient data selected
            if (inds.length <= 1) {return}
            
            else {
                for (var key in var_meta) {

                    y = []                    
                    var y_comp = []

                    for (var i = 0; i < inds.length; i++) {
                        y.push(data[key][inds[i]])                         
                        y_comp.push(data[select.value][inds[i]])                        
                    } 
                    
                    
                    if (select_dist.value == "dtw"){dist = dtwDist(y, y_comp)}
                    else if (select_dist.value == "euclid"){dist = euclid(y, y_comp)}

                    summary_data["variable"].push(key)
                    summary_data["dist"].push(parseFloat(dist.toFixed(3)))
                    selected_data["variable"].push(key)
                    selected_data["y"].push(y)
                                        
                }
            
            }
            cds_selection_summary_data.data["variable"] = summary_data["variable"]
            cds_selection_summary_data.data["dist"] = summary_data["dist"]
            
            cds_tsplot.change.emit();
            cds_selection_summary_data.change.emit();
"""


div_head = """
<div style="font-size:12px; font-family:helvetica; color:grey; margin-left: 0px; width: 900px; float: left;">

<p>
An interactive time series exploration tool built using <a href="https://bokeh.org/" target="_blank" class="url">Bokeh</a> and <a href="https://d3js.org/" target="_blank" class="url">D3.js</a>.
This is a static standalone Bokeh dashboard with all the data embedded in the .html file. All computations and interactive callsbacks are happening client side using javascript. 
The interactive analysis approach shown here can be useful for detecting patterns and anomalies in multivariate time series. Here I have visualized the S&P100 stock prices.
</p>

<p>
Use the box select tool in the plot below to select a segment of the time series to analyze:
  <ul>
    <li>
      Run linear regression for all variables over the selected segment to identify trends. I used the 
      <a href="https://cdnjs.com/libraries/jstat" class="url" target="_blank">jstat</a> library for this
    </li>
    
    <li>
      Sort by regression slope over selected segments, number of upper/lower control limit violations, etc. using the data table
    </li>
    
    <li>
      Calculate <a href="https://en.wikipedia.org/wiki/Dynamic_time_warping" target="_blank" class="url">Dynamic Time Wrapping<a> or Euclidean distance for the selected variable segment against all other variables. You may then sort by distance to identify the most similar segments
      The dynamic time wrapping implementation was taken from Gordon Lesti's <a class="url" target="_blank" href="https://github.com/GordonLesti/dynamic-time-warping">work</a>
    </li>
    
    <li>
      Compute agglomerative <a href="https://en.wikipedia.org/wiki/Hierarchical_clustering#:~:text=In%20data%20mining%20and%20statistics,build%20a%20hierarchy%20of%20clusters." target="_blank" class="url">heirarchical clustering</a> for selected segments and display results in a d3.js dendrogram.
      The clustering implementation was adapted from Stephen Oni's <a class="url" target="_blank" href="https://becominghuman.ai/hierarchical-clustering-in-javascript-brief-introduction-2f88e8601362">work.</a>
      Segment amplitudes are normalized to be between 0 and 1 prior to distance calculation and clustering
    </li>
    
    <li>
      The d3 dendrogram code was adapted from Mike Bostock's <a target="_blank" class="url" href="https://bl.ocks.org/d3noob/8375092">blog</a>
      Hover over parent nodes to see the average shape of for a given cluster overlayed on top of shapes from all child nodes. 
      This can be useful for understanding what all the child nodes have in common and how homogenous a given cluster is
    </li>
  </ul>


</div>
"""


div_social = """
<div class="header" style="style=font-size:12px; font-family:helvetica; color:grey; margin-left: 0px; margin-bottom: 0px; width: 400px; float: left;">
 <a href="https://www.linkedin.com/in/hnagib?_l=en_US" target="_blank" class="fa fa-linkedin" style="font-size:24px"></a>
 <a href="https://github.com/hnagib" class="fa fa-github" target="_blank" style="font-size:24px"></a>
 <a href="https://www.facebook.com/bigannasah/" target="_blank" class="fa fa-facebook" style="font-size:24px"></a>
 <a href="https://www.instagram.com/hnagib/" target="_blank" class="fa fa-instagram" style="font-size:24px"></a>
 <a href="https://twitter.com/HasanNagib/" target="_blank" class="fa fa-twitter" style="font-size:24px"></a>
 <a href="mailto:hasan.nagib@gmail.com?subject = Hasan's fitness data blog&body = Hello!" class="fa fa-envelope" style="font-size:24px"></a>
</div>
"""