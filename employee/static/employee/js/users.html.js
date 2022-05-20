let select = $('#show');
select.change('change', function () {
    let search = $('#search_text').val();
    if (search === '') {
        window.location.href = '/employee/users/search//' + select.val() + '/1';
    } else {
        let filter = $('#filter').val();
        let splitInSearch = window.location.href.split(`${filter}=${search}`);
        window.location.href = `${splitInSearch[0]}${filter}=${search}/${select.val()}/1`;
    }
});

function updateStatus(checkbox, id) {
    let action = confirm('Are you sure you want to ' + ((checkbox.checked) ? 'activate' : 'deactivate') + ' this user account ?');
    if (action) {
        let reason = prompt('The reason ?');
        if (reason) {
            $.ajax({
                url: window.location.href,
                type: 'POST',
                data: {
                    'csrfmiddlewaretoken': getCookie('csrftoken'),
                    'id': id,
                    'is_active': (checkbox.checked) ? 1 : 0,
                    'reason': reason
                },
                dataType: 'json',
                success: function (response) {
                    if (!response.error_msg) {
                        alert('User account has been ' + ((response.is_active) ? 'activated' : 'deactivated') + ' successfully.');
                    }
                }
            });
            return;
        } else {
            alert('You need to specify the reason.');
        }
    }
    checkbox.checked = !checkbox.checked;
}

$('#search').click(function () {
    let search = $('#search_text').val();
    let splitInSearch = window.location.href.split('/search/');
    if (search === '') {
        window.location.href = `${splitInSearch[0]}/search//10/1`;
    } else {
        let filter = $('#filter').val();
        if (filter === ''){
            alert('Choose a search filter');
            return;
        }
        window.location.href = `${splitInSearch[0]}/search/${filter}=${search}/${splitInSearch[1].split('/')[1]}/1`;
    }
});
