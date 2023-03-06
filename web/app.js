google.charts.load('current', {
  packages: ['corechart', 'line']
});
google.charts.setOnLoadCallback(drawChart);

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

async function getFile(filePath) {
  const response = await fetch(filePath);
  const data = await response.json();
  return data;
}

function drawChart() {
  const chart = new google.visualization.LineChart(document.getElementById('chart_div'));
  const fs = parseInt(window.getComputedStyle(document.getElementById('download_btn')).fontSize);
  const dict = getFile("data/data.json");

  /*const file = loadFile("data/data.json");
  const dict = JSON.parse(file);*/

  let arr = [];

  for (let key of Object.keys(dict)) {
    arr.push([new Date(key), dict[key].moisture, dict[key].temp]);
  }

  arr.sort(function(a, b) {
    return b[0] - a[0];
  });

  let data = new google.visualization.DataTable();
  data.addColumn('datetime', 'X');
  data.addColumn('number', 'Fuktighet');
  data.addColumn('number', 'Temperatur');

  data.addRows(arr);

  const options = {
    hAxis: {
      title: 'Tid'
    },
    backgroundColor: '#F0F0F0',
    colors: ['#243B10', '#3B1210'],
    curveType: 'function',
    fontName: 'Raleway',
    fontSize: fs,
    legend: {position: 'bottom'}
  };

  chart.draw(data, options);
}