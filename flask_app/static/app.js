// const Chart = require('chart.js');

// function updateChart() {
//     // fetch data
//     async function fetchData() {
//         console.log('********** in fetchData ***************')
//         const url = "http://127.0.0.1:5000/data";
//         // get response
//         const response = await fetch(url)
//         // wait for completed request
//         const datapoints = await response.json();
//         console.log('**************')
//         console.log(datapoints)
//         return datapoints
//     }
//     const data = {
//         labels: [],
//         totals: []
//     }

//     fetchData().then(datapoints => {
//         console.log('**************************')
//         console.log('in fetchData')
//         console.log(datapoints)
//         for (const datapoint of datapoints) {
//             console.log("*************datapoints**********")
//             console.log(datapoint)
//             data.labels.push(datapoint['category'])
//             data.totals.push(datapoint['total'])
//         }
//     })
//     console.log('!!!!!!!!!!!!!!! data !!!!!!!!!!')
//     console.log(data)
//     return data;
// }


// expenses = updateChart();

// const data = {
//     labels: expenses.labels,
//     datasets: [{
//         label: 'My First Dataset',
//         data: expenses.data,
//         backgroundColor: [
//             'rgb(255, 99, 132)',
//             'rgb(54, 162, 235)',
//             'rgb(255, 205, 86)'
//         ],
//         hoverOffset: 4
//     }]
// };
// const config = {
//     type: 'doughnut',
//     data: data,
// };


// const myChart = new Chart(
//     document.getElementById('my-chart'), config
// );