google.charts.load('current', {
  packages: ['corechart', 'line']
});
google.charts.setOnLoadCallback(drawCharts);

async function getFile(filePath) {
  const response = await fetch(filePath);
  const data = await response.json();
  return data;
}

function getLineChart(chartId) {
  const chart = new google.visualization.LineChart(document.getElementById(chartId));
  return chart;
}

function getDataTable(dict, colNr, type, name) {
  const dt = new google.visualization.DataTable();
  dt.addColumn('datetime', 'X');
  dt.addColumn(type, name);

  const arr = [];
  for (let entry of dict["data"].slice(-100)) {
    arr.push([new Date(entry[0]), entry[colNr]])
  }
  dt.addRows(arr);

  const fmt_d = new google.visualization.DateFormat({pattern: 'EEEE d MMM HH:mm:ss'});
  fmt_d.format(dt, 0);

  return dt
}

function drawCharts() {
  const m_chart = getLineChart('m_chart_div');
  const t_chart = getLineChart('t_chart_div');

  const dict = getFile("data/data.json");

  const m_data = getDataTable(dict, 1, 'number', 'Jordfuktighet');
  const t_data = getDataTable(dict, 2, 'number', 'Lufttemperatur');

  const fmt_m = new google.visualization.NumberFormat({pattern:'##.#', suffix: '%'});
  const fmt_t = new google.visualization.NumberFormat({pattern: '##.#°C'});

  fmt_m.format(m_data, 1);
  fmt_t.format(t_data, 1);

  const em = parseInt(window.getComputedStyle(document.getElementById('download_btn')).fontSize);

  const options = {
    title: 'Title',
    backgroundColor: '#F0F0F0',
    colors: ['#243B10', '#3B1210'],
    curveType: 'function',
    fontName: 'Raleway',
    fontSize: em,
    legend: 'none',
    chartArea:{left: '8%', right: '2%', width:'90%'},
  };

  m_chart.draw(m_data, {...options, title: 'Jordfuktighet'});
  t_chart.draw(t_data, {...options, title: 'Lufttemperatur'});
}