var graphSentiment = document.getElementById('plotSentiment');
var graphPrice = document.getElementById('plotPrice');

console.log(graphSentiment)
console.log(graphPrice)

var trace1 = {
    mode: 'lines',
    type: 'scatter'
};

var trace2 = {
  yaxis: 'y2',
  mode: 'lines',
  type: 'scatter'
};

var sentimentLayout = {
  title: 'Historical Finndex Score',
  xaxis: {
      title: 'Date',
      showgrid: false,
      zeroline: false
    },
  yaxis: {
      title: 'Finndex Score',
      showline: false
  },
  yaxis2: {
    title: 'Price',
    titlefont: {color: 'rgb(148, 103, 189)'},
    tickfont: {color: 'rgb(148, 103, 189)'},
    overlaying: 'y',
    side: 'right'
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
 * Retrieves sentiment data from the finndex API.
 * 
 * @param coin the ticker symbol for the coin to be retrieved
 * @param startDate the date from which the API search will begin, formatted as YYYY-mm-dd
 * @param endDate the date at which the API search will end, formatted as YYYY-mm-dd
 * @param metrics the string array containing the metric IDs (e.g. 'trends', 'fear_and_greed')
 * @param weights the float array containing the weights
 */
function retrieveSentimentData(coin, startDate, endDate, metrics, weights) {
  apiFormatted = "http://44.233.186.17:9200/api/sentiment/coin=" + coin + "?start_date=" + startDate 
                  + "&end_date=" + endDate + "&metrics=" + metrics.join() + "&weights=" + weights.join();

  let request = new XMLHttpRequest();
  request.open("GET", apiFormatted);
  request.send();

  return request;
}

/**
 * Retrieves price data from the finndex API.
 * 
 * @param coin the ticker symbol for the coin to be retrieved
 * @param startDate the date from which the API search will begin, formatted as YYYY-mm-dd
 * @param endDate the date at which the API search will end, formatted as YYYY-mm-dd
 */
function retrievePriceData(coin, startDate, endDate) {
  apiFormatted = "http://44.233.186.17:9200/api/price/coin=" + coin + "?start_date=" + startDate 
                  + "&end_date=" + endDate;

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
  
  requestSentiment = retrieveSentimentData(coin, startDate, endDate, metrics, weights);

  requestSentiment.onload = () => {
    if (requestSentiment.status == 200) {// success 
      obj = JSON.parse(requestSentiment.response);

      x = [];
      y = [];
      for (var key in obj) {
        x.push(key);
        y.push(parseFloat(obj[key]));
      }
    
      trace2.x = x;
      trace2.y = y;
      
      requestPrice = retrievePriceData(coin, startDate, endDate);

      requestPrice.onload = () => {
        if (requestPrice.status == 200) {// success 
          obj = JSON.parse(requestPrice.response);
    
          x = [];
          y = [];
          for (var key in obj) {
            x.push(key);
            y.push(parseFloat(obj[key]));
          }
        
          trace1.x = x;
          trace1.y = y;
        
          Plotly.newPlot(graphSentiment, [trace1, trace2], sentimentLayout);
        } 
        else {
            console.log(`Error ${requestPrice.status}: ${requestPrice.statusText}`)
        }
      };
    } 
    else {
        console.log(`Error ${requestSentiment.status}: ${requestSentiment.statusText}`)
    }
  };
}