var winWidth = window.innerWidth;

console.log(winWidth);

// define margins and canvas
var svg = d3.select("svg"),
  margin = {
    top: 20,
    right: 80,
    bottom: 30,
    left: 70
  },
  elWidth = svg.attr("width"),
  width = +elWidth - margin.left - margin.right;

console.log(elWidth);

var height = svg.attr("height") - margin.top - margin.bottom,
  g = svg.append("g").attr("transform", "translate(" + margin.left + "," +
    margin.top + ")");

// sample: 2017-01-05T09:06:40.670Z
var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S.%L%Z");

// loop over data, coercing types
data.forEach((each) => {
  each.fields.value = +each.fields.value;
  each.fields.date_time = parseTime(each.fields.date_time)
})

console.log(data);

// define y scale
var y = d3.scaleTime().range([0, height]);

// define y scale domain
y.domain(d3.extent(data, function(d) {
  return d.fields.date_time;
}));

// map the ordinal values (0,1) to discrete colors
var color = d3.scaleOrdinal()
  .range(["white", "maroon"])
  .domain([0, 1]);

var barWidth = height / data.length;

console.log(barWidth);

var barGroups = g.selectAll("g")
  .data(data)
  .enter().append("g")
  .attr("transform", function(d, i) {
    // return `translate(0, ${i * barWidth})`
    return `translate(0, ${ y(d.fields.date_time)})`

  });

barGroups.append("rect")
  .attr("fill", (d) => {
    return color(d.fields.value);
  })
  .attr("height", barWidth)
  .attr("width", width);

// define yAxis here because we need to customize
var yAxis = d3.axisLeft(y)
  .ticks(30);

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
