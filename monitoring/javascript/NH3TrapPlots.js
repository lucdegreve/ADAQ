
function drawNH3TrapPlots(csvfile){
    
    var color = d3.scaleOrdinal(d3.schemeCategory10);
    
    var parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");
    
    var margin = {top: 30, right: 30, bottom: 170, left: 30},
        margin2 = {top: 360, right: 30, bottom: 70, left: 30},
        width = 600 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;
        height2 = 500 - margin2.top - margin2.bottom;    

    var x = d3.scaleTime().range([0, width]);
    var x2 = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);
    var y2 = d3.scaleLinear().range([height2, 0]);

    var xAxis = d3.axisBottom(x),
        xAxis2 = d3.axisBottom(x2),
        yAxis = d3.axisLeft(y);

    var lineT1 = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.T1); });
   
    var lineT1_brush = d3.line()
        .x(function(d) { return x2(d.Datetime); })
        .y(function(d) { return y2(d.T1); });
 
    var lineT2 = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.T2); });
    
    var lineT3 = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.T3); });
    
    var lineT4 = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.T4); });
    
    var lineTA = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.T_A); });
    
    var lineTT = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.T_T); });
    
    var lineDP1 = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.DP1); });
    
    var lineDP2 = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.DP2); });
    
    var lineDP3 = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.DP3); });
    
    var lineDP4 = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.DP4); });
    
    var lineDPT = d3.line()
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.DP_T); });
    
    
    var svgT = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
   

    svgT.append("defs").append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", width)
        .attr("height", height);


    var focus = svgT.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var context = svgT.append("g")
      .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

    // brush stuff

    var brush = d3.brushX()
        .extent([[0, 0], [width, height2]])
        .on("end", brushed);
 
    d3.csv(csvfile, function(error, data) {
      if (error) throw error;
    
      data.forEach(function(d) {
        d.Datetime = parseDate(d.Datetime);
        });
   
      first = new d3.extent(data, function(d) { return d.Datetime; })[0]
      last = new d3.extent(data, function(d) { return d.Datetime; })[1];
      now = new Date();

      x.domain(d3.extent(data, function(d) { return d.Datetime;}));
      y.domain([10,30]);
    
      x2.domain(x.domain());
      y2.domain(y.domain());
      
 
      focus.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(1))
          .attr("d", lineT1);
      
      context.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(1))
          .attr("d", lineT1_brush);
 
      focus.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(2))
          .attr("d", lineT2);
    
      focus.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(3))
          .attr("d", lineT3);
    
      focus.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(4))
          .attr("d", lineT4);
    
      focus.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(5))
          .attr("d", lineTT);
    
      focus.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(6))
          .attr("d", lineTA);
     
      focus.append("g")
          .attr("class", "axis axis--x")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      context.append("g")
          .attr("class", "axis axis--x")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis2);


      // Add brush to context
       context.append("g")
            .attr("class", "x brush")
            .call(brush)
          .selectAll("rect")
            .attr("y", -6)
            .attr("height", height2 + 7);



      // draw legend
      var legend = svgT.selectAll(".legend")
          .data(color.domain())
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });
    
      // draw legend colored rectangles
      legend.append("rect")
          .attr("x", width + 18)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color);
    
      // draw legend text
      legend.append("text")
          .attr("x", width + 8)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(function(d) { return d;})
    
      var tick = svgT.append("g")
          .attr("class", "axis axis--y")
          .call(d3.axisLeft(y))
        .select(".tick:last-of-type");
    
    
    });
    
    
    var svgDP = d3.select("body").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    
    d3.csv(csvfile, function(error, data) {
      if (error) throw error;
    
      data.forEach(function(d) {
        d.Datetime = parseDate(d.Datetime);
        });
   
      console.log(JSON.stringify(data));
 
      x.domain(d3.extent(data, function(d) { return d.Datetime;}));
      y.domain([
    
          Math.min(-10000, d3.min(data, function(d){ return d.DP1}), 
                           d3.min(data, function(d){ return d.DP2}),
                           d3.min(data, function(d){ return d.DP3}),
                           d3.min(data, function(d){ return d.DP4}),
                           d3.min(data, function(d){ return d.DP_T})),
          Math.max(0, d3.max(data, function(d){ return d.DP1}), 
                           d3.max(data, function(d){ return d.DP2}),
                           d3.max(data, function(d){ return d.DP3}),
                           d3.max(data, function(d){ return d.DP4}),
                           d3.max(data, function(d){ return d.DP_T}))]);
    
      svgDP.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(1))
          .attr("d", lineDP1);
    
      svgDP.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(2))
          .attr("d", lineDP2);
    
      svgDP.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(3))
          .attr("d", lineDP3);
    
      svgDP.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(4))
          .attr("d", lineDP4);
    
      svgDP.append("path")
          .data([data])
          .attr("class", "line")
          .style("stroke", color(5))
          .attr("d", lineDPT);
       
      svgDP.append("g")
          .attr("class", "axis axis--x")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x));
    
      // draw legend
      var legend = svgDP.selectAll(".legend")
          .data(color.domain())
        .enter().append("g")
          .attr("class", "legend")
          .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });
    
      // draw legend colored rectangles
      legend.append("rect")
          .attr("x", width + 18)
          .attr("width", 18)
          .attr("height", 18)
          .style("fill", color);
    
      // draw legend text
      legend.append("text")
          .attr("x", width + 8)
          .attr("y", 9)
          .attr("dy", ".35em")
          .style("text-anchor", "end")
          .text(function(d) {return d;})
    
      var tick = svgDP.append("g")
          .attr("class", "axis axis--y")
          .call(d3.axisLeft(y))
        .select(".tick:last-of-type");

        // initial brush

        oneDayAgo = d3.utcDay.offset(now, -1);
        brushSel = context.append('g').call(brush);
        brush.move(brushSel, [oneDayAgo, now].map(x));
    
    
    });

    function brushed() {

      var s = d3.event.selection; // || x2.range();
      x.domain(s.map(x2.invert, x2));

      //focus.selectAll("path.line")
      //    .attr("d",  function(d) {return lineT1(d)})
      //    .attr("d",  function(d) {return lineT2(d)})
      //    .attr("d",  function(d) {return lineT3(d)});
      //focus.select(".axis--x").call(xAxis);
    }
}
