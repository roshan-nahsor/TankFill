// console.log('Hello World')
// $(document).ready(function(){

// });


// const ctx = document.getElementById('myChart');


// var graphData={
//     type: 'bar',
//     data: {
//         labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//         datasets: [{
//         label: '# of Votes',
//         data: [12, 19, 3, 5, 2, 3],
//         borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//         y: {
//             beginAtZero: true
//         }
//         }
//     }
//     }

// var myChart =new Chart(ctx, graphData);


var socket=new WebSocket('ws://127.0.0.1:8000/ws/tank/');

socket.onmessage = function(e){
    var djangoData=JSON.parse(e.data);
    console.log(djangoData);
// document.write("reached here");

    // var newGraphData=graphData.data.datasets[0].data;
    // newGraphData.shift();
    // newGraphData.push(djangoData.value);
    
    // graphData.data.datasets[0].data=newGraphData;
    // myChart.update();

    document.querySelector('#app').innerText=djangoData.value;
}
