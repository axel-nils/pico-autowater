google.charts.load('current', {
  packages: ['corechart', 'line']
});
google.charts.setOnLoadCallback(drawTemps);

function drawTemps() {

  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'X');
  data.addColumn('number', 'Temperatur');

  data.addRows([
    [new Date(2023, 2, 5, 8), 20],
    [new Date(2023, 2, 5, 12), 22],
    [new Date(2023, 2, 5, 16), 23],
  ]);

  var options = {
    title: 'Hittepådata',
    hAxis: {
      title: 'Tid'
    },
    vAxis: {
      title: 'Celsius'
    },
    backgroundColor: '#F0F0F0',
    colors: ['#243B10'],
    curveType: 'function',
    fontName: 'Raleway'
  };

  var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

  chart.draw(data, options);
}