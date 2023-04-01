google.charts.load("current", {packages: ["corechart", "gauge"], "language": "sv"}).then(drawCharts);
window.onload = (event) => {
  getWeatherJson(weatherUrl)
};

const em = parseInt(window.getComputedStyle(document.getElementById("download_btn")).fontSize);
const gaugeSize = parseInt(window.getComputedStyle(document.getElementById("on_btn")).width);
const green = "#243B10";
const red = "3B1210";
const white = "#F8F8F8";
const weatherUrl = "https://api.openweathermap.org/data/2.5/weather?id=6943587&units=metric&lang=se&appid=87d1bfdb974592195531cdf4aae52fd2";

function getIntFromElementId(id) {
  const maybeInt = parseInt(document.getElementById(id).textContent);
  return isNaN(maybeInt) ? 0 : maybeInt;
}

async function getWeatherJson(url) {
  const response = await fetch(url);
  const json = await response.json();
  const description = json.weather[0].description;
  const temp = parseInt(json.main.temp);
  document.getElementById("weather").innerHTML = temp + " °C och " + description;
}

async function getDataJson(filePath) {
  const response = await fetch(filePath);
  return await response.json();
}

const lineChartOptions = {
  chartArea: {width: "90%"},
  backgroundColor: green,
  colors: [white],
  fontSize: em,
  fontName: "Raleway",
  titleTextStyle: {
    color: white, fontName: "Marcellus", bold: false
  },
  vAxis: {
    gridlines: {count: 0},
    textStyle: {color: white},
    textPosition: "in"
  },
  hAxis: {
    format: "EEE",
    gridlines: {color: white},
    minorGridlines: {count: 0},
    textStyle: {color: white},
  },
  legend: {position: "none"}
};


const gaugeOptions = {
  width: 0.9 * gaugeSize, height: 0.9 * gaugeSize,
  redFrom: 0, redTo: getIntFromElementId("dry_string"),
  greenColor: green, greenFrom: getIntFromElementId("wet_string"), greenTo: 100,
};

function getLineChart(chartId) {
  return new google.visualization.LineChart(document.getElementById(chartId));
}

function getDataTable(data_array, colNr, type, name) {
  const dt = new google.visualization.DataTable();
  dt.addColumn("datetime", "X");
  dt.addColumn(type, name);

  const arr = [];
  for (let entry of data_array) {
    arr.push([new Date(entry[0]), entry[colNr]])
  }
  dt.addRows(arr);

  const fmt_d = new google.visualization.DateFormat({pattern: "EEEE d MMM HH:mm"});
  fmt_d.format(dt, 0);

  return dt
}

async function drawCharts() {
  const data_json = await getDataJson("data.json")
  const data_array = data_json.data;

  const g_chart =new google.visualization.Gauge(document.getElementById("gauge_div"));
  const g_data = google.visualization.arrayToDataTable([
    ["Label", "Value"],
    ["Fuktighet", getIntFromElementId("moisture_string")]]);
  g_chart.draw(g_data, gaugeOptions);

  const m_chart = getLineChart("m_chart_div");
  const m_data = getDataTable(data_array, 1, "number", "Jordfuktighet");
  const fmt_m = new google.visualization.NumberFormat({pattern:"##.#", suffix: "%"});
  fmt_m.format(m_data, 1);
  m_chart.draw(m_data, {...lineChartOptions, title: "Jordfuktighet [%]"});

  const t_chart = getLineChart("t_chart_div");
  const t_data = getDataTable(data_array, 2, "number", "Lufttemperatur");
  const fmt_t = new google.visualization.NumberFormat({pattern: "##.#°C"});
  fmt_t.format(t_data, 1);
  t_chart.draw(t_data, {...lineChartOptions, title: "Lufttemperatur [°C]"});
}