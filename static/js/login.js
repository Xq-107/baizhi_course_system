$(function () {
    //用户名为空时不提示
    $("[name='username']").keyup(function () {
        $(".user_error").css("display", "none");
    });
    //密码为空时不提示
    $("[name='pwd']").keyup(function () {
        $(".pwd_error").css("display", "none");
    });
    //用户名光标离开后检验密码是否合法
    $("[name='username']").blur(function () {
        var username = $("[name='username']").val();
        var regex = /^[\u4E00-\u9FA5]{2,10}$/;
        var result = regex.test(username);
        if (result) {
            $(".user_error").css("display", "none");
        }
        else if ($(this).val() === "") {
            $(".user_error").html("用户名不能为空");
            $(".user_error").css("display", "inline-block");
        }
        else {
            $(".user_error").html("用户名必须为2到10位中文名称！");
            $(".user_error").css("display", "inline-block");
        }
    });
    //密码光标离开后检验密码是否合法
    $("[name='pwd']").blur(function () {
        if (18 >= $(this).val().length >= 6) {
            var regex = /^(\w){6,18}$/;
            var result = regex.test($(this).val());
            if (result) {
                $(".pwd_error").css("display", "none");
            } else {
                $(".pwd_error").html("密码必须为6到18位字母、数字或下划线");
                $(".pwd_error").css("display", "inline-block");
            }
        }
        else if ($(this).val() === "") {
            $(".pwd_error").html("密码不能为空");
            $(".pwd_error").css("display", "inline-block");
        }
        else if ($(this).val().length < 6 || $(this).val().length > 18) {
            $(".pwd_error").html("密码长度必须为6到18位");
            $(".pwd_error").css("display", "inline-block");
        }
    });
});