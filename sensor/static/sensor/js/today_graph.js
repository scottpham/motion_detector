// define margins and canvas
var svg = d3.select("svg"),
  margin = {
    top: 20,
    right: 80,
    bottom: 30,
    left: 70
  },
  width = svg.attr("width") - margin.left - margin.right,
  height = svg.attr("height") - margin.top - margin.bottom,
  g = svg.append("g").attr("transform", "translate(" + margin.left + "," +
    margin.top + ")");

// 2017-01-05T09:06:40.670Z
var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S.%L%Z");

// loop over data, coercing types
data.forEach((each) => {
  each.fields.value = +each.fields.value;
  each.fields.date_time = parseTime(each.fields.date_time)
})

console.log(data);

// define scales
var x = d3.scaleTime().range([0, width]),
  y = d3.scaleLinear().range([height, 0]);

// define line
var line = d3.line()
  .x(function(d) {
    return x(d.fields.date_time);
  })
  .y(function(d) {
    return y(+d.fields.value);
  });

// define x scale domain
x.domain(d3.extent(data, function(d) {
  return d.fields.date_time;
}));

console.log(d3.extent(data, function(d) {
  return d.fields.date_time;
}));

var ticks = [0, 1];
var tickLabels = ["Still", "Motion"]

// set y scale domain
y.domain(ticks);

// append x axis to canvas
g.append("g")
  .attr("class", "axis axisx")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x)); //define x axis on the fly, anon

// append line
g.append("path")
  .datum(data)
  .attr("class", "line")
  .attr("d", line)
  .style("stroke", "maroon");

// define yAxis here because we need to customize
var yAxis = d3.axisLeft(y)
  .tickValues(ticks)
  .tickFormat(function(d, i) {
    return tickLabels[i];
  });

// append y axis to canvas
g.append("g")
  .attr("class", "axis axisy")
  .call(yAxis)
  .append("text")
  .attr("class", "label");

d3.selectAll(".axisy text")
  // .attr("transform", "rotate(-45)")
  // .attr("y", "-20px")
  // .attr("x", "20px")
  // .dy("-1em")
