$(function () {
    //设置默认时间
    var id1 = setTimeout(function () {
        var now = new Date();
        var year = now.getFullYear();
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
        var day = ("0" + now.getDate()).slice(-2);
        var hours = ("0" + now.getHours()).slice(-2);
        var minutes = ("0" + now.getMinutes()).slice(-2);
        $(".local_time").val(year + "-" + month + "-" + day + "T" + hours + ":" + minutes)
    }, 1);
    var id2 = setInterval(function () {
        var now = new Date();
        var year = now.getFullYear();
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
        var day = ("0" + now.getDate()).slice(-2);
        var hours = ("0" + now.getHours()).slice(-2);
        var minutes = ("0" + now.getMinutes()).slice(-2);
        $(".local_time").val(year + "-" + month + "-" + day + "T" + hours + ":" + minutes)
    }, 60000);
});