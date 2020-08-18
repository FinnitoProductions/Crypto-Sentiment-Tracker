var graphDiv = document.getElementById('plot');

var trace1 = {
    x: [1, 2, 3, 4,5,6,7,8,9,10],
    y: [0.5,0.54,0.56,0.54,0.53,0.48,0.46,0.59,0.62,0.58],
    mode: 'lines',
    type: 'scatter'
};

var layout = {
  title: 'Historical Finndex Score',
  xaxis: {
      title: 'Date',
      showgrid: false,
      zeroline: false
    },
  yaxis: {
      title: 'Finndex Score',
      showline: false
  }
};

populateDateDropdowns("start_date", 10);
populateDateDropdowns("end_date", 0);
updateGraph();

/**
 * Populates a date dropdown box with dates from the most recent year, offset back by a given value.
 * 
 * @param id the HTML ID of the dropdown box to be populated
 * @param offset the integer value of the offset 
 */
function populateDateDropdowns(id, offset) {
  var select = document.getElementById(id);

  var startDate = new Date(); // today

  dates = []
  for (var i = 365 + offset; i > offset; i--)
  {
    newDate = new Date(startDate.getTime());
    newDate.setDate(startDate.getDate() - i);
    newDate = newDate.getFullYear() + "-" + ('0' + (newDate.getMonth() + 1)).slice(-2) + "-" + ('0' + newDate.getDate()).slice(-2);

    var el = document.createElement("option");
    el.textContent = newDate;
    el.value = newDate;
    select.appendChild(el);
  }
}

/**
 * Retrieves data from the finndex API.
 * 
 * @param coin the ticker symbol for the coin to be retrieved
 * @param startDate the date from which the API search will begin, formatted as YYYY-mm-dd
 * @param endDate the date at which the API search will end, formatted as YYYY-mm-dd
 * @param metrics the string array containing the metric IDs (e.g. 'trends', 'fear_and_greed')
 * @param weights the float array containing the weights
 */
function retrieveAPIData(coin, startDate, endDate, metrics, weights) {
  apiFormatted = "http://44.233.186.17:9200/api/sentiment/coin=" + coin + "?start_date=" + startDate 
                  + "&end_date=" + endDate + "&metrics=" + metrics.join() + "&weights=" + weights.join();

  let request = new XMLHttpRequest();
  request.open("GET", apiFormatted);
  request.send();

  return request;
}

/**
 * Updates the given plot by pulling data from the form displayed beneath the graph.
 */
function updateGraph() {
  coinDropdown = document.getElementById("coins");
  coin = coinDropdown.options[coinDropdown.selectedIndex].value;

  startDateDropdown = document.getElementById("start_date");
  startDate = startDateDropdown.options[startDateDropdown.selectedIndex].value;

  endDateDropdown = document.getElementById("end_date");
  endDate = endDateDropdown.options[endDateDropdown.selectedIndex].value;

  boxes = document.getElementsByClassName("weightsField");
  metrics = []
  weights = []
  for (var i = 0; i < boxes.length; i++) {
    if (boxes[i].value != 0.0) {
      metrics.push(boxes[i].id)
      weights.push(boxes[i].value)
    }
  }
  
  request = retrieveAPIData(coin, startDate, endDate, metrics, weights);

  request.onload = () => {
    if (request.status == 200) {// success 
      obj = JSON.parse(request.response);

      x = [];
      y = [];
      for (var key in obj) {
        x.push(key);
        y.push(parseFloat(obj[key]));
      }
    
      trace1.x = x;
      trace1.y = y;
    
      console.log(trace1);
    
      Plotly.newPlot(graphDiv, [trace1], layout);
    } 
    else {
        console.log(`Error ${request.status}: ${request.statusText}`)
    }
  };
}

  
  