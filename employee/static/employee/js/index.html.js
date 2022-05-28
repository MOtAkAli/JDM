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
            one_color_chart('line', 'Earnings', response.months, response.monthly_earnings, canvas_id);
        },
    });
}

function one_color_chart(chart_type, label, labels, values, canvas_id) {
    const chart_data = {
        labels: labels,
        datasets: [{
            label: label,
            backgroundColor: 'rgb(78, 115, 223)',
            borderColor: 'rgb(78, 115, 223)',
            data: values,
        }]
    };

    const chart_config = {
        type: chart_type,
        data: chart_data,
        options: {
            barPercentage: 0.25
        }
    };

    const chart = new Chart(
        document.getElementById(canvas_id),
        chart_config
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

function multi_colors_chart(chart_type, label, labels, values, canvas_id) {
    const chart_data = {
        labels: labels,
        datasets: [{
            label: label,
            data: values,
            backgroundColor: rgb_colors_gen(labels.length),
            hoverOffset: 4
        }]
    };

    const chart_config = {
        type: chart_type,
        data: chart_data,
    };

    const chart = new Chart(
        document.getElementById(canvas_id),
        chart_config
    );
}
