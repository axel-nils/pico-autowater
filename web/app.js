google.charts.load('current', {
  packages: ['corechart', 'line']
});
google.charts.setOnLoadCallback(drawCharts);

const em = parseInt(window.getComputedStyle(document.getElementById('download_btn')).fontSize);

const chartOptions = {
  backgroundColor: '#F0F0F0',
  colors: ['#243B10', '#3B1210'],
  fontName: 'Raleway',
  fontSize: em,
  legend: 'none',
  theme: 'maximized',
};

async function getJson(filePath) {
  const response = await fetch(filePath);
  const json = await response.json();
  console.log(json)
  console.log(json.data)
  return json.data;
}

function getLineChart(chartId) {
  const chart = new google.visualization.LineChart(document.getElementById(chartId));
  return chart;
}

function getDataTable(data_array, colNr, type, name) {
  const dt = new google.visualization.DataTable();
  dt.addColumn('datetime', 'X');
  dt.addColumn(type, name);

  const arr = [];
  for (let entry of data_array) {
    arr.push([new Date(entry[0]), entry[colNr]])
  }
  dt.addRows(arr);

  const fmt_d = new google.visualization.DateFormat({pattern: 'EEEE d MMM HH:mm:ss'});
  fmt_d.format(dt, 0);

  return dt
}

async function drawCharts() {
  const data_array = await getJson('data/data.json');
  console.log(data_array)

  const m_chart = getLineChart('m_chart_div');
  const m_data = getDataTable(data_array, 1, 'number', 'Jordfuktighet');
  const fmt_m = new google.visualization.NumberFormat({pattern:'##.#', suffix: '%'});
  fmt_m.format(m_data, 1);
  m_chart.draw(m_data, chartOptions);

  const t_chart = getLineChart('t_chart_div');
  const t_data = getDataTable(data_array, 2, 'number', 'Lufttemperatur');
  const fmt_t = new google.visualization.NumberFormat({pattern: '##.#°C'});
  fmt_t.format(t_data, 1);
  t_chart.draw(t_data, chartOptions);
}