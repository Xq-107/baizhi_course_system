$(function () {
    //用户名获取光标时不提示
    $("[name='user_name']").focus(function () {
        $(".user_error")[0].style.display = "none";
    });
    //邮箱获取光标时不提示
    $("[name='email']").focus(function () {
        $(".error_tip")[0].style.display = "none";
    });


    //用户名失去光标时对用户名进行正则验证
    $("[name='user_name']").blur(function () {
        var username = $(this).val();
        var regex = /^[\u4E00-\u9FA5]{2,10}$/;
        var result = regex.test(username);
        if (result) {
            $(".user_error")[0].style.display = "display";
        }
        else if ($(this).val() === "") {
            $(".user_error")[0].innerHTML = "用户名不能为空";
            $(".user_error")[0].style.display = "inline-block";
        }
        else {
            $(".user_error")[0].innerHTML = "用户名必须为2到10位中文名称";
            $(".user_error")[0].style.display = "inline-block";
        }
    });

    //邮箱失去光标时对用户名进行正则验证
    $("[name='email']").blur(function () {
        var regex = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
        var result = regex.test($(this).val());
        if (result) {
            $(".error_tip")[0].style.display = "none";
        } else {
            $(".error_tip")[0].innerHTML = "请输入正确的邮箱格式";
            $(".error_tip")[0].style.display = "inline-block";
        }
    });
});