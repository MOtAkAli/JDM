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
    checkbox_checked = checkbox.checked;
    Swal.fire({
        title: 'Are you sure?',
        text: 'You want to ' + ((checkbox_checked) ? 'activate' : 'deactivate') + ' this user account ?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#4e73df',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes',
        allowOutsideClick: false,
    }).then((result) => {
        if (result.isConfirmed) {
            bootbox.prompt({
                title: "The reason ?",
                inputType: 'textarea',
                maxlength: 500,
                centerVertical: true,
                callback: function (reason) {
                    if (reason) {
                        $.ajax({
                            url: window.location.href,
                            type: 'POST',
                            data: {
                                'csrfmiddlewaretoken': getCookie('csrftoken'),
                                'id': id,
                                'is_active': (checkbox_checked) ? 1 : 0,
                                'reason': reason
                            },
                            dataType: 'json',
                            success: function (response) {
                                if (!response.error_msg) {
                                    Swal.fire({
                                        title: 'User account ' + ((response.is_active) ? 'activated' : 'deactivated'),
                                        icon: 'success',
                                        confirmButtonColor: '#4e73df',
                                    })
                                }
                            }
                        });
                        console.log('after');
                        return;
                    } else if (reason === '') {
                        Swal.fire({
                            title: 'The reason is required',
                            icon: 'error',
                            confirmButtonColor: '#4e73df',
                        })
                        checkbox.checked = !checkbox_checked;
                    } else {
                        checkbox.checked = !checkbox_checked;
                    }
                }
            });
        } else {
            checkbox.checked = !checkbox_checked;
        }
    })
}

$('#search').click(function () {
    let search = $('#search_text').val();
    let splitInSearch = window.location.href.split('/search/');
    if (search === '') {
        window.location.href = `${splitInSearch[0]}/search//10/1`;
    } else {
        let filter = $('#filter').val();
        if (filter === '') {
            alert('Choose a search filter');
            return;
        }
        window.location.href = `${splitInSearch[0]}/search/${filter}=${search}/${splitInSearch[1].split('/')[1]}/1`;
    }
});
