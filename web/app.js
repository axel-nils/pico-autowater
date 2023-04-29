const em = parseInt(window.getComputedStyle(document.getElementById("download_btn")).fontSize);
const green = "rgba(36,59,16,0.75)";
const faintGreen = "rgba(36,59,16,0.1)";
const red = "rgba(255,0,0,0.75)";
const yellow = "rgba(255,234,0,0.75)";
const white = "#F8F8F8";
const black = "rgba(16,16,16,1)";
const wetLevel = getIntFromElementId("wet_string", 90)
const dryLevel = getIntFromElementId("dry_string", 50)
const isDry = (ctx, value) => ctx.p0.parsed.y < dryLevel && ctx.p1.parsed.y < dryLevel ? value : undefined;
const isWet = (ctx, value) => ctx.p0.parsed.y > wetLevel && ctx.p1.parsed.y > wetLevel ? value : undefined;

window.onload = (event) => {
  getWeatherJson(weatherUrl)
};

const weatherUrl = "https://api.met.no/weatherapi/nowcast/2.0/complete?lat=57.4&lon=12.0"
const legendUrl = "https://api.met.no/weatherapi/weathericon/2.0/legends"

async function getWeatherJson() {
  const weatherRespone = await fetch(weatherUrl);
  const weatherJSON = await weatherRespone.json();
  const weatherData = weatherJSON.properties.timeseries[0].data;
  const temperature = parseInt(weatherData.instant.details.air_temperature);
  const weatherCode = weatherData.next_1_hours.summary.symbol_code;
  const legendResponse = await fetch(legendUrl);
  const legendJSON = await legendResponse.json();
  const description = legendJSON[weatherCode.split("_")[0]].desc_nb.toLowerCase();
  document.getElementById("weather").innerHTML = "Utomhus är det " + temperature + "°C och " + description + ".";
}

function getIntFromElementId(id, def) {
  const maybeInt = parseInt(document.getElementById(id).textContent);
  return isNaN(maybeInt) ? def : maybeInt;
}

async function getDataJson(filePath) {
  const response = await fetch(filePath);
  return await response.json();
}

Chart.defaults.font.size = em;
Chart.defaults.font.family = "Raleway, consolas";
Chart.defaults.color = "#101010";
Chart.defaults.plugins.legend.display = false;

async function drawMainChart() {
  const rawData = await getDataJson("data.json")
  const ctx = document.getElementById("mainCanvas").getContext('2d');

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
        ticks: {
          callback: x => x + "%"
        },
        grid: {
          drawOnChartArea: false
        },
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
        grid: {
          drawOnChartArea: false
        },
      },
      y_s2: {
        stack: 'stack',
        stackWeight: 2,
        position: 'right',
        offset: true,
        type: 'category',
        labels: ['ON', 'OFF'],
        grid: {
          drawOnChartArea: false
        },
      },
      y_t: {
        stack: "stack",
        stackWeight: 5,
        position: 'right',
        ticks: {
          callback: x => x + ' °C'
        },
        grid: {
          drawOnChartArea: false
        },
        suggestedMin: 20,
        suggestedMax: 30,
      }
    }
  }

  function tickFilter(value) {
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

function drawGaugeChart() {
  x = getIntFromElementId("moisture_string", 73);
  var ctx = document.getElementById("gaugeCanvas").getContext('2d')
  Chart.overrides.doughnut.rotation = 240;
  Chart.overrides.doughnut.circumference = 240;
  Chart.overrides.doughnut.cutout = "80%";
  Chart.overrides.doughnut.borderColor = "rgba(0,0,0,0)"
  const data = {
    labels: false,
    datasets: [{
      backgroundColor: [red, yellow, green],
      data: [dryLevel, wetLevel - dryLevel, 100 - wetLevel],
      weight: 1
    },
      {
        backgroundColor: ["rgba(0,0,0,1)", "rgba(0,0,0,0)"],
        data: [x, 100 - x],
        weight: 2,
        borderRadius: {
          outerEnd: em,
          innerEnd: em
        }
      }
    ]
  }

  const opt = {
    responsive: true,
    aspectRatio: 1.5,
    plugins: {
      tooltips: {
        enabled: false
      },
      title: {
        display: true,
        text: x.toString() + "%",
        position: "bottom"
      }
    }
  }

  const config = {
    type: 'doughnut',
    data: data,
    options: opt
  }
  new Chart(ctx, config);
}

drawMainChart()
drawGaugeChart()
