//var searchInfo = $.getJSON("scrapedInfo.json");
//var searchInfo = require('./scrapedInfo.json')
//var searchInfo = JSON.parse("scrapedInfo.json");
let jsonData;


fetch('static/js/scrapedInfo.json')
.then((response) =>  response.json())
.then(data => {
    jsonData = data;
    console.log(jsonData);
    for(let i=0;i<jsonData[0].length;i++){
        div = document.createElement("div");
        document.getElementById("searchResults").innerHTML += jsonData[0][i] 
        +"<br> <img src=' "+jsonData[1][i]+"' >"
        +"<br> <b>"+jsonData[2][i]+"</b> <br>"
        +jsonData[3][i]
        +"<br>"+jsonData[4][i]+"<br><br>";
        document.createElement("div");
        
    }
})

//searchDocument.getElementById("searchResults").innerHTML;
//function printResults()
//{
    
//}