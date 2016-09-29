$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
$(function() {
    $(window).bind("load resize", function() {
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.sidebar-collapse').addClass('collapse')
        } else {
            $('div.sidebar-collapse').removeClass('collapse')
        }
    })
    $('#btnlogin').click(function () {
        var username = $('#username').val();
        var passwd = $('#passwd').val();
        $.ajaxSetup({
            data: { csrfmiddlewaretoken: csrf_token },
        });
        $.post('/admin/ajaxlogin', { username: username, passwd: passwd }, function (d) {
            if (d.errcode == 0) {
                window.location = '/admin/index';
            } else {
                alert(d.msg);
            }
        });
    });
})