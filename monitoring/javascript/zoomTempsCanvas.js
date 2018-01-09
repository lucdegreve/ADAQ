
function drawTempsCanvas(csvfile, title){    
    
    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 100, bottom: 170, left: 30},
        margin2 = {top: 360, right: 30, bottom: 70, left: 30},
        width = 600 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom,
        height2 = 500 - margin2.top - margin2.bottom;
    
    
    // set the colour scale
    var color = d3.scaleOrdinal(d3.schemeCategory10);
    
    // Parse the date / time
    var parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");
    
    // Set the ranges
    var x = d3.scaleTime().range([0, width]);  
    var x2 = d3.scaleTime().range([0, width]);  
    var y = d3.scaleLinear().range([height, 0]);
    var y2 = d3.scaleLinear().range([height2, 0]);
    
    var xAxis = d3.axisBottom(x),
        xAxis2 = d3.axisBottom(x2),
        yAxis = d3.axisLeft(y);
    
    // Define the line
    var templine = d3.line()	
        .x(function(d) { return x(d.Datetime); })
        .y(function(d) { return y(d.T); });
       
    var templine2 = d3.line()        
        .x(function(d) { return x2(d.Datetime); })
        .y(function(d) { return y2(d.T); });
 
    // Adds the svg canvas
    var svg = d3.select("body")
        .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
        .append("g")
            .attr("transform", 
                  "translate(" + margin.left + "," + margin.top + ")");
    
    svg.append("defs").append("clipPath")
        .attr("id", "clip")
      .append("rect")
        .attr("width", width)
        .attr("height", height);
    
    
    var focus = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
          
    var context = svg.append("g")
      .attr("transform", "translate(" + margin2.left + "," + margin2.top + ")");

    // brush stuff

    var brush = d3.brushX()
        .extent([[0, 0], [width, height2]])
        .on("end", brushed);

    // Legend stuff
    var legendRectSize = 18;
    var legendSpacing = 4;
 
    // Get the data
    d3.csv(csvfile, function(error, data) {
    
        data.forEach(function(d) {
    		d.Datetime = parseDate(d.Datetime);
        });
    
        // Scale the range of the data

        first = new d3.extent(data, function(d) { return d.Datetime; })[0]
        last = new d3.extent(data, function(d) { return d.Datetime; })[1];
        now = new Date();

        x.domain([first, now]);
        y.domain([-10, 90]);
   
        x2.domain(x.domain());
        y2.domain(y.domain());
    
        var dataByProbe = d3.nest()
          .key(function(d) { return d.probe; })
          .entries(data);
    
        var focuslineGroups = focus.selectAll("g")
            .data(dataByProbe)
            .enter()
            .append("g");
          
        var focuslines = focuslineGroups.append("path")
            .attr("class","line")
            .attr("d", function(d) { return templine(d.values); })
            .style("stroke", function(d) {return color(d.key);})
            .attr("clip-path", "url(#clip)");
    
        focus.append("g") 
            .attr("class", "axis axis--x")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
     
        focus.append("g")
            .attr("class", "y axis")
            .call(yAxis);
    
        var contextlineGroups = context.selectAll("g")
            .data(dataByProbe)
          .enter().append("g");
        
        var contextLines = contextlineGroups.append("path")
            .attr("class", "line")
            .attr("d", function(d) { return templine2(d.values); })
            .style("stroke", function(d) {return color(d.key);})
            .attr("clip-path", "url(#clip)");
     
        context.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height2 + ")")
            .call(xAxis2);
     
        context.append("g")
            .attr("class", "x brush")
            .call(brush)
          .selectAll("rect")
            .attr("y", -6)
            .attr("height", height2 + 7);


        // legend
        dataByProbe.forEach( function (item)
        {
            
            var legx = width+margin.left+10;
            var legy = item.key * (legendRectSize+legendSpacing);
            svg.append('rect')
              .attr("x", legx)
              .attr("y", legy)                                     
              .attr('width', legendRectSize)                         
              .attr('height', legendRectSize)                       
              .style('fill', color(item.key))                               
              .style('stroke', color(item.key));

            svg.append('text')            
              .attr('x', legx + legendRectSize + legendSpacing)
              .attr('y', legy + legendRectSize - legendSpacing)
              .text(parseInt(item.key));        

        });


        // Add the title
        svg.append("text")
                    .attr("x", (width / 2))             
                    .attr("y", 0 - (margin.top / 2))
                    .attr("text-anchor", "middle")  
                    .style("font-size", "16px") 
                    .style("text-decoration", "underline")  
                    .text(title);
            
            
        // Add the text label for the Y axis
        svg.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 0 - margin.left)
            .attr("x",0 - (height / 2))
            .attr("dy", "1em")
            .style("text-anchor", "middle")
            .text("T°");
   
        // initial brush

        oneDayAgo = d3.utcDay.offset(now, -1); 
        brushSel = context.append('g').call(brush);       
        brush.move(brushSel, [oneDayAgo, now].map(x));


        });

    function brushed() {
    
      var s = d3.event.selection; // || x2.range();
      x.domain(s.map(x2.invert, x2));

      focus.selectAll("path.line").attr("d",  function(d) {return templine(d.values)});
      focus.select(".axis--x").call(xAxis);
    }
}
