google.charts.load('current', {
  packages: ['corechart', 'line']
});
google.charts.setOnLoadCallback(drawTemps);

function loadFile(filePath) {
  var result = null;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", filePath, false);
  xmlhttp.send();
  if (xmlhttp.status==200) {
    result = xmlhttp.responseText;
  }
  return result;
}

function drawTemps() {

  const file = loadFile("data/data.json");
  console.log(file);

  const dict = JSON.parse(file);
  console.log(dict)

  var arr = [];

  for (let key of Object.keys(dict)) {
    arr.push([new Date(key), dict[key].moisture / 10, dict[key].temp]);
  }

  arr.sort(function(a, b) {
    return b[0] - a[0];
  });

  console.log(arr)

  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'X');
  data.addColumn('number', 'Fuktighet');
  data.addColumn('number', 'Temperatur');

  data.addRows(arr);

  var options = {
    title: 'Riktig data',
    hAxis: {
      title: 'Tid'
    },
    vAxis: {
      title: 'Celsius'
    },
    backgroundColor: '#F0F0F0',
    colors: ['#243B10', '#3B1210'],
    curveType: 'function',
    fontName: 'Raleway'
  };

  var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

  chart.draw(data, options);
}