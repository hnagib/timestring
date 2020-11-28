template = """
<!DOCTYPE html>
<html lang="en">
{% block head %}
  	<!-- Load d3.js -->
    <script src="https://d3js.org/d3.v4.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/jstat@latest/dist/jstat.min.js"></script>
    <script src="dtw.js"></script>
    <script src="cluster.js"></script>
    
<head>
    {% block inner_head %}
    <meta charset="utf-8">

  <head>
    <style>
    .h1 {
    style=font-family:helvetica; 
    color:grey; 
    font-size:28px; 
    font-weight:bold;
    margin-top: 10px; 
    }
    .text {
        style=font-family:helvetica; 
        color:grey; 
        float: left;
        margin-top: 10px; 
    }
    .h2 {
        style=font-family:helvetica; 
        color:grey; 
        font-size:16px; 
        font-weight:bold;
        margin-top: 10px; 
    }

    .para {
        style=font-family:helvetica;
        font-size:12px; 
        color:grey; 
        margin-left: 40px; 
        width: 400px; 
        float: left;
    }

    .node {
        cursor: pointer;
    }

    .node circle {
      fill: #43658B;
      stroke: #495464;
      stroke-width: 3px;
    }

    .node text {
      font: 12px sans-serif;
    }

    .link {
      fill: none;
      stroke: #BBBFCA;
      stroke-width: 3px;
    }

    a.url:link {
      color: #e73360;
      background-color: transparent;
      text-decoration: none;
    }

    a.url:visited {
      color: #e73360;
      background-color: transparent;
      text-decoration: none;
    }

    a.url:hover {
      color: #154ba6;
      background-color: transparent;
      text-decoration: none;
    }

    a.url:active {
      color: #e73360;
      background-color: transparent;
      text-decoration: underline;
    }
    
    </style>

  </head>

  <body>

<!-- load the d3.js library --> 
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js"></script>
    
    
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
var treeData = [clust]

// ************** Generate the tree diagram  *****************
d3.select("svg").remove();

var margin = {top: 20, right: 120, bottom: 20, left: 120},
    width = 2000 - margin.right - margin.left,
    height = 1000 - margin.top - margin.bottom;
    
var i = 0,
    duration = 1200,
    root;

var tree = d3.layout.tree()
    .size([height, width]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

var svg = d3.select("body").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

root = treeData[0];
root.x0 = height / 2;
root.y0 = 0;
  
update(root);

d3.select(self.frameElement).style("height", "100px");

function update(source) {

  // Compute the new tree layout.
  var nodes = tree.nodes(root).reverse(),
      links = tree.links(nodes);

  // Normalize for fixed-depth.
  nodes.forEach(function(d) { d.y = d.depth * 100; });

  // Update the nodes…
  var node = svg.selectAll("g.node")
      .data(nodes, function(d) { return d.id || (d.id = ++i); });

  // Enter any new nodes at the parent's previous position.
  var nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
      .on("click", click);

  nodeEnter.append("circle")
      .attr("r", 1e-6)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#BBBFCA"; })
      .on("click", click_leaf);

  nodeEnter.append("text")
      .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
      .attr("dy", ".35em")
      .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
      .text(function(d) { return d.name; })
      .style("fill-opacity", 1e-6);

  // Transition nodes to their new position.
  var nodeUpdate = node.transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

  nodeUpdate.select("circle")
      .attr("r", 10)
      .style("fill", function(d) { return d._children ? "lightsteelblue" : "#BBBFCA"; });

  nodeUpdate.select("text")
      .style("fill-opacity", 1);

  // Transition exiting nodes to the parent's new position.
  var nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
      .remove();

  nodeExit.select("circle")
      .attr("r", 1e-6);

  nodeExit.select("text")
      .style("fill-opacity", 1e-6);

  // Update the links…
  var link = svg.selectAll("path.link")
      .data(links, function(d) { return d.target.id; });

  // Enter any new links at the parent's previous position.
  link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", function(d) {
        var o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      });

  // Transition links to their new position.
  link.transition()
      .duration(duration)
      .attr("d", diagonal);

  // Transition exiting nodes to the parent's new position.
  link.exit().transition()
      .duration(duration)
      .attr("d", function(d) {
        var o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      })
      .remove();

  // Stash the old positions for transition.
  nodes.forEach(function(d) {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

// Toggle children on click.
function click(d) {
  if (d.children) {
    d._children = d.children;
    d.children = null;
  } else {
    d.children = d._children;
    d._children = null;
  }
  update(d);
}

// Toggle children on click.
function click_leaf(d) {
  if (d.children) {
    
  } else {
    console.log("--->"+d["name"])
    if(d["name"] != "") {select.value = d["name"]}
  }
  update(d);
}


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
                    y_usl_breach = []
                    y_lsl_breach = []
                    
                    y_comp = []

                    for (var i = 0; i < inds.length; i++) {{
                        y.push(data[key][inds[i]])
                        
                        y_comp.push(data[select.value][inds[i]])
                        
                        y_usl_breach.push(data[key][inds[i]] >= data[key+"_usl"][inds[i]])
                        y_lsl_breach.push(data[key][inds[i]] <= data[key+"_lsl"][inds[i]])
                        
                        x.push([1, inds[i]])
                    }} 
                    
                    
                    m = jStat.models.ols(y,x).coef[1];     
                    
                    summary_data["variable"].push(key)
                    summary_data["slope"].push(parseFloat((m*inds.length).toFixed(3)))
                    summary_data["usl"].push(y_usl_breach.filter((value) => value).length)
                    summary_data["lsl"].push(y_lsl_breach.filter((value) => value).length)
                    summary_data["dist"].push(parseFloat(dist.toFixed(3)))
                    
                    selected_data["variable"].push(key)
                    selected_data["y"].push(y)
                                        
                }}
            
            }}
            cds_selection_summary_data.data["variable"] = summary_data["variable"]
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
                    y_comp = []

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
<h1 class="h1">TimeString</h1>
<div style="font-size:12px; font-family:helvetica; color:grey; margin-left: 40px; width: 700px; float: left;">

<p>
An interactive time series exploration tool built using <a href="https://bokeh.org/" target="_blank" class="url">Bokeh</a> and <a href="https://d3js.org/" target="_blank" class="url">D3.js</a>.
This is served as a static standalone Bokeh dashboard. All computations are performed client side using javascript. 
Select a segment of the time series to analyze. 
</p>

<p>
Features:
  <ul>
    <li>Runs linear regression for all variables over the selected segment to identify trends</li>
    <li>Sort by regression slope over selected segments, number of upper/lower control limit violations, etc. using the data table</li>
    <li>Calculate <a href="https://en.wikipedia.org/wiki/Dynamic_time_warping" target="_blank" class="url">Dynamic Time Wrapping<a> or Euclidean distance for the selected variable segment against all other variables. You may then sort by distance to identify the most similar segments</li>
    <li>Compute agglomerative <a href="https://en.wikipedia.org/wiki/Hierarchical_clustering#:~:text=In%20data%20mining%20and%20statistics,build%20a%20hierarchy%20of%20clusters." target="_blank" class="url">heirarchical clustering</a> for selected segments and display results in a d3.js dendrogram</li>
    <li>Click on dendrogram leaf to inspect the corresponding segment</li>
  </ul>
</p>
</div>
"""