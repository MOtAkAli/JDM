function getCookie(name) {
    let cookies = document.cookie.split('; ');
    let needed = undefined;
    cookies.forEach(cookie => {
        let cookieArray = cookie.split('=');
        if (cookieArray[0] === name) {
            needed = cookieArray[1];
        }
    });
    return needed;
}
