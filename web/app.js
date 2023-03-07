google.charts.load('current', {
  packages: ['corechart', 'line']
});
google.charts.setOnLoadCallback(drawCharts);

async function getFile(filePath) {
  const response = await fetch(filePath);
  const data = await response.json();
  return data;
}

function drawCharts() {
  const m_chart = new google.visualization.LineChart(document.getElementById('m_chart_div'));
  const t_chart = new google.visualization.LineChart(document.getElementById('t_chart_div'));
  const em = parseInt(window.getComputedStyle(document.getElementById('download_btn')).fontSize);
  const dict = getFile("data/data.json");

  const m_arr = [];
  const t_arr = [];

  for (let entry of dict["data"].slice(-100)) {
    m_arr.push([new Date(entry.d), entry.m])
    t_arr.push([new Date(entry.d), entry.t])
  }

  const m_data = new google.visualization.DataTable();
  m_data.addColumn('datetime', 'X');
  m_data.addColumn('number', 'Jordfuktighet');
  m_data.addRows(m_arr);

  const t_data = new google.visualization.DataTable();
  t_data.addColumn('datetime', 'X');
  t_data.addColumn('number', 'Lufttemperatur');
  t_data.addRows(t_arr);

  const fmt_d = new google.visualization.DateFormat({pattern: 'EEEE d MMM HH:mm:ss'});
  const fmt_m = new google.visualization.NumberFormat({pattern:'##.#', suffix: '%'});
  const fmt_t = new google.visualization.NumberFormat({pattern: '##.#°C'});

  fmt_d.format(m_data, 0);
  fmt_d.format(t_data, 0);
  fmt_m.format(m_data, 1);
  fmt_t.format(t_data, 1);

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