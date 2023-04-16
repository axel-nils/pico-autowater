google.charts.load("current", {packages: ["gauge"], "language": "sv"}).then(drawCharts);

const em = parseInt(window.getComputedStyle(document.getElementById("download_btn")).fontSize);
const gaugeSize = parseInt(window.getComputedStyle(document.getElementById("on_btn")).width);
const green = "rgba(36,59,16,0.75)";
const faintGreen = "rgba(36,59,16,0.1)";
const red = "rgba(255,0,0,0.75)";
const yellow = "rgba(255,234,0,0.75)";
const white = "#F8F8F8";
const black = "rgba(16,16,16,1)";
const wetLevel = getIntFromElementId("wet_string")
const dryLevel = getIntFromElementId("dry_string")

function getIntFromElementId(id) {
  const maybeInt = parseInt(document.getElementById(id).textContent);
  return isNaN(maybeInt) ? 0 : maybeInt;
}

async function getDataJson(filePath) {
  const response = await fetch(filePath);
  return await response.json();
}

const gaugeOptions = {
  width: 0.9 * gaugeSize, height: 0.9 * gaugeSize,
  redFrom: 0, redTo: dryLevel,
  greenColor: green, greenFrom: wetLevel, greenTo: 100,
};

async function drawCharts() {
  const g_chart =new google.visualization.Gauge(document.getElementById("gauge_div"));
  const g_data = google.visualization.arrayToDataTable([
    ["Label", "Value"],
    ["Fuktighet", getIntFromElementId("moisture_string")]]);
  g_chart.draw(g_data, gaugeOptions);
}

async function chartIt() {
  const rawData = await getDataJson("data.json")
  const ctx = document.getElementById('myChart').getContext('2d');
  Chart.defaults.font.size = em;
  Chart.defaults.font.family = "Raleway, consolas";
  Chart.defaults.color = "#101010";
  Chart.defaults.plugins.legend.display = false;
  const ms = rawData.data.map(d => Object({
    x: d[0],
    y: d[1]
  }));
  const ts = rawData.data.map(d => Object({
    x: d[0],
    y: d[2]
  }));
  const ss = rawData.data.map(d => Object({
    x: d[0],
    y: d[3] === true ? "ON" : "OFF"
  }));

  const data = {
    datasets: [{
      label: "Bevattning",
      data: ss,
      yAxisID: 'y_s',
      borderColor: black,
      pointStyle: false,
      stepped: true
    }, {
      label: "Jordfuktighet",
      data: ms,
      yAxisID: 'y_m',
      borderColor: black,
      segment: {
        borderColor: (ctx) => isDry(ctx, red) || isWet(ctx, green) || yellow
      },
      pointStyle: false,
    }, {
      label: "Temperatur",
      data: ts,
      yAxisID: 'y_t',
      backgroundColor: faintGreen,
      fill: true,
      showLine: false,
      pointStyle: false,
    }]
  }

  const opt = {
    responsive: true,
    aspectRatio: 1.5,
    scales: {
      x: { // TODO properly implement dates https://www.chartjs.org/docs/latest/samples/scales/time-line.html
        ticks: {
          callback: tickFilter,
          align: 'start'
        }
      },
      y_m: {
        stack: "stack",
        stackWeight: 5,
        position: 'left',
        ticks: { callback: x => x + "%" },
        grid: { drawOnChartArea: false },
        suggestedMin: 0,
        suggestedMax: 100,
      },
      y_s: {
        stack: 'stack',
        stackWeight: 2,
        position: 'left',
        offset: true,
        type: 'category',
        labels: ['ON', 'OFF'],
        grid: { drawOnChartArea: false },
      },
      y_s2: {
        stack: 'stack',
        stackWeight: 2,
        position: 'right',
        offset: true,
        type: 'category',
        labels: ['ON', 'OFF'],
        grid: { drawOnChartArea: false },
      },
      y_t: {
        stack: "stack",
        stackWeight: 5,
        position: 'right',
        ticks: { callback: x => x + ' °C' },
        grid: { drawOnChartArea: false },
        suggestedMin: 20,
        suggestedMax: 30,
      }
    }
  }
  const isDry = (ctx, value) => ctx.p0.parsed.y < dryLevel && ctx.p1.parsed.y < dryLevel ? value : undefined;
  const isWet = (ctx, value) => ctx.p0.parsed.y > wetLevel && ctx.p1.parsed.y > wetLevel ? value : undefined;


  function tickFilter(value, index, values) {
    const date = new Date(this.getLabelForValue(value))
    const weekday = date.toLocaleDateString('sv-SE', {
      weekday: 'short'
    })
    return date.getHours() === 0 ? weekday : null
  }

  const cfg = {
    type: 'line',
    data: data,
    options: opt
  }

  const chart = new Chart(ctx, cfg);
}
chartIt()
