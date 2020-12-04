function plot_cluster(treeData, var_meta, select) {


  d3.select("svg").remove();
  d3.select(".d3-tip").remove();

  var tool_tip = d3.tip()
  .attr("class", "d3-tip")
  .offset([-35, 10])
  .html("<div id='var_meta'></div><div id='banana'></div>");


  var margin = {top: 20, right: 120, bottom: 20, left: 120},
      width = 4000 - margin.right - margin.left,
      height = 2000 - margin.top - margin.bottom;
      
  var i = 0,
      duration = 1000,
      root;

  var tree = d3.layout.tree()
      .size([height, width]);

  var diagonal = d3.svg.diagonal()
      .projection(function(d) { return [d.y, d.x]; });

  var svg = d3.select("body").append("svg")
      .attr("width", width + margin.right + margin.left)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .call(tool_tip)

  root = treeData;
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
      .on("mouseover", function(d) {tipplot(d, tool_tip, var_meta)})
      .on("mouseout", tool_tip.hide)
      .on("click", click)


  nodeEnter.append("circle")
      .attr("r", 1e-6)
      .on("click", click_leaf)

  
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
      .style("fill", function(d) { return d._children ? "#495464" : (d["name"] != "")? var_meta[d["name"]]["color"] : "#F6F6F6"; })


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

}


function tipplot(d, tool_tip, var_meta) {

      tool_tip.show()
      
      //The data for our line

      var hover_ys_list = []
      var hover_y = []
      var lineData = []
 
      if (Array.isArray(d['vec'][0])) {
        var hover_y = norm(d['vec'][0])
        var hover_ys_long = flatten([d['vec'][1], d['vec'][2]])
        

        var i,j,temparray, avgarray, chunk = hover_y.length;
        for (i=0,j=hover_ys_long.length; i<j; i+=chunk) {
            temparray = hover_ys_long.slice(i,i+chunk);
            hover_ys_list.push(norm(temparray))
        }

        var test = []
        for (var i = 0; i < hover_ys_list[0].length; i++) {
           var sum = 0;
           for (var j = 0; j < hover_ys_list.length; j++)
           {
              sum = sum + hover_ys_list[j][i];
           }
           var avg = sum / hover_ys_list.length;
           
           test.push(avg)

        }


      }
      else {
        var hover_y = norm(d['vec'])
        var test = norm(df['vec'])
      }
      
      var tipSVG = d3.select("#banana")
        .append("svg")
        .attr("width", 400)
        .attr("height", 100);

      for (var j = 0; j < hover_ys_list.length; j++) {
        
        lineData = []
        
        for (var k = 0; k < hover_ys_list[j].length; k++) {
          lineData.push({"x":(50+(300*(k+1))/(hover_ys_list[j].length)), "y":10+80*(1-norm(hover_ys_list[j])[k])})
        }

        
        //This is the accessor function we talked about above
        var lineFunction = d3.svg.line()
                                 .x(function(d) { return d.x; })
                                 .y(function(d) { return d.y; })
                                 .interpolate("linear");

        tipSVG.append("path")
        .attr("d", lineFunction(lineData))
        .attr("stroke", "black")
        .attr("stroke-width", 2)
        .style("opacity", 0.25)
        .attr("fill", "none");
      }



      lineData = []
      hover_y = test

      for (var i = 0; i < hover_y.length; i++) {
        lineData.push({"x":(50+(300*(i+1))/(hover_y.length)), "y":10+80*(1-hover_y[i])})
      }
      
      //This is the accessor function we talked about above
      var lineFunction = d3.svg.line()
                               .x(function(d) { return d.x; })
                               .y(function(d) { return d.y; })
                               .interpolate("linear");


      tipSVG.append("path")
      .attr("d", lineFunction(lineData))
      .attr("stroke", "#dd2c00")
      .attr("stroke-width", 4)
      .style("opacity", .9)
      .attr("fill", "none");

      document.getElementById("var_meta").innerHTML = `
      <br></br>
      <p class='hovertext'>
      <ul>
      <li><b>Name</b>: ${var_meta[d["name"]]["desc"]}</li>
      <li><b>Category</b>: ${var_meta[d["name"]]["category"]}</li>
      </ul>
      </p>
      `
  }


