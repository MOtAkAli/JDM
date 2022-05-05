const select = document.getElementById('show');
select.addEventListener('change', function () {
    window.location.href = '/employee/users/' + select.value + '/1';
});