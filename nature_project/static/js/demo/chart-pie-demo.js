// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
document.addEventListener("DOMContentLoaded", function() {
    var ctxPie = document.getElementById("myPieChart");
    var myPieChart = new Chart(ctxPie, {
        type: 'doughnut',
        data: {
            labels: ["Reservado", "En ejecución", "Cancelado", "Confirmado"],
            datasets: [{
                data: [{{ count_booking }}, {{ count_booking2 }}, {{ count_booking3 }}, {{ count_booking4 }}],
                backgroundColor: ['#4e73df', '#1cc88a', '#e74a3b', '#f6c23e'],
                hoverBackgroundColor: ['#2e59d9', '#17a673', '#e74a3b', '#f6c23e'],
                hoverBorderColor: "rgba(234, 236, 244, 1)",
            }],
        },
        options: {
            maintainAspectRatio: false,
            tooltips: {
                backgroundColor: "rgb(255,255,255)",
                bodyFontColor: "#858796",
                borderColor: '#dddfeb',
                borderWidth: 1,
                xPadding: 15,
                yPadding: 15,
                displayColors: false,
                caretPadding: 10,
            },
            legend: {
                display: false
            },
            cutoutPercentage: 80,
        },
    });
});
