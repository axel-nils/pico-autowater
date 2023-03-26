google.charts.load('current', {packages: ['corechart'], 'language': 'sv'}).then(drawCharts);
window.onload = (event) => {
  getWeatherJson(weatherUrl)
};

const em = parseInt(window.getComputedStyle(document.getElementById('download_btn')).fontSize);
const color = '#243B10';
const white = '#F8F8F8';
const weatherUrl = 'https://api.openweathermap.org/data/2.5/weather?id=6943587&units=metric&lang=se&appid=87d1bfdb974592195531cdf4aae52fd2';

const chartOptions = {
  chartArea: {width: '100%', top: 0, bottom: 2*em},
  backgroundColor: color,
  colors: [white],
  fontSize: em,
  fontName: 'Raleway',
  vAxis: {
    gridlines: {count: 0},
    textStyle: {color: white},
    textPosition: 'in'
  },
  hAxis: {
    format: 'EEE',
    gridlines: {color: white, count: 6},
    textStyle: {color: white},
  }
};

async function getWeatherJson(url) {
  const response = await fetch(url);
  const json = await response.json();
  const desc = json.weather[0].description;
  const temp = parseInt(json.main.temp);
  document.getElementById("weather").innerHTML = temp + ' °C och ' + desc;
}

async function getDataJson(filePath) {
  const response = await fetch(filePath);
  const json = await response.json();
  return json;
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

  const fmt_d = new google.visualization.DateFormat({pattern: 'EEEE d MMM HH:mm'});
  fmt_d.format(dt, 0);

  return dt
}

async function drawCharts() {
  const data_json = await getDataJson('data.json')
  const data_array = data_json.data;

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