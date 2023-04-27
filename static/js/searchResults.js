//var searchInfo = $.getJSON("scrapedInfo.json");
//var searchInfo = require('./scrapedInfo.json')
//var searchInfo = JSON.parse("scrapedInfo.json");


let jsonData;
//currentPage = window.location.href.split().pop();
currentPage = parseInt(window.location.href.substring(window.location.href.indexOf("/search") + 8));
//fetch('../static/js/scrapedInfo.json')
fetch('../../../static/js/scrapedInfo.json')
.then((response) =>  response.json())
.then(data => {
    jsonData = data;
    
    const sortRow = 2;

// Get the values of the sort row
    const sortValues = jsonData[sortRow];

    const sortIndices = Array.from(sortValues.keys());
    sortIndices.sort((a, b) => sortValues[a] - sortValues[b]);
    const sortedArr = jsonData.map(row => sortIndices.map(index => row[index]));
     
    jsonData = sortedArr;


    console.log(sortedArr);
    for(let i=0;i<jsonData[0].length;i++){
        div = document.createElement("div");
        document.getElementById("searchResults").innerHTML += jsonData[0][i] 
        +"<br> <img src=' "+jsonData[1][i]+"' >"
        +"<br> <b>"+jsonData[2][i]+"</b> <br>"
        +jsonData[3][i]
        +"<br>"+"<a href='"+jsonData[4][i]+"'>"+jsonData[4][i]+"</a><br><br>";
    }
    currentURL = window.location.href.slice(0,window.location.href.lastIndexOf("/search"));
    document.getElementById("pageButtons").innerHTML = 
    '<a href='+currentURL+'/search/'+(currentPage-1)+' class="previous">&laquo; Previous</a>'+
    '<a href='+currentURL+'/search/'+(currentPage+1)+' class="next">Next &raquo;</a>';
    
})

//searchDocument.getElementById("searchResults").innerHTML;
//function printResults()
//{
    
//}