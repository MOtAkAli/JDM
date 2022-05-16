function remove_add_canvas(container, canvas_id) {
    $(`#${canvas_id}`).remove();
    $(`#${container}`).append(`<canvas id="${canvas_id}"></canvas>`);
}

let reservations_select = $('#reservations_year_select');
reservations_select.change(function () {
    canvas_id = 'reservations_monthly_chart';
    remove_add_canvas('reservations_monthly_chart_div', canvas_id);
    get_stats('reservations', reservations_select.val(), canvas_id);
});

function get_stats(which_one, year, canvas_id) {
    $.ajax({
        url: window.location.href,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'which_one': which_one,
            'year': year,
        },
        dataType: 'json',
        success: function (response) {
            $('#monthly_earning').text(`${response.monthly_earning} DH`);
            reservations_monthly_chart(response.months, response.monthly_earnings, canvas_id);
        },
    });
}

function reservations_monthly_chart(months, values, canvas_id) {
    const monthly_data = {
        labels: months,
        datasets: [{
            label: 'Earnings',
            backgroundColor: 'rgb(78, 115, 223)',
            borderColor: 'rgb(78, 115, 223)',
            data: values,
        }]
    };

    const monthlyConfig = {
        type: 'line',
        data: monthly_data,
        options: {}
    };

    const monthly_chart = new Chart(
        document.getElementById(canvas_id),
        monthlyConfig
    );
}

function random_number(max = 256) {
    return Math.floor(Math.random() * max);
}

function rgb_colors_gen(count) {
    let rgbs = []
    for (let i = 0; i < count; i++) {
        rgbs.push('rgb(' + random_number() + ', ' + random_number() + ', ' + random_number() + ')');
    }
    return rgbs;
}

function reservations_annually_chart(years, values, canvas_id) {
    const annually_data = {
        labels: years,
        datasets: [{
            label: 'My First Dataset',
            data: values,
            backgroundColor: rgb_colors_gen(years.length),
            hoverOffset: 4
        }]
    };

    const annually_config = {
        type: 'pie',
        data: annually_data,
    };

    const annually_chart = new Chart(
        document.getElementById(canvas_id),
        annually_config
    );
}
