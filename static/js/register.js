$(function () {
    //用户名获取光标时不提示
    $("[name='user_name']").focus(function () {
        $(".error_tip")[0].style.display = "none";
    });
    //密码获取光标时不提示
    $("[name='pwd']").focus(function () {
        $(".error_tip")[1].style.display = "none";
    });
    //确定密码获取光标时不提示
    $("[name='cpwd']").focus(function () {
        $(".error_tip")[2].style.display = "none";
    });
    //邮箱获取光标时不提示
    $("[name='email']").focus(function () {
        $(".error_tip")[3].style.display = "none";
    });
    //验证码获取光标时不提示
    $("[name='captcha']").focus(function () {
        $(".error_tip")[4].style.display = "none";
    });
    //复选框协议单击
    $("[name='allow']").click(function () {
        if ($("[name='allow']").is(':checked')) {
            $(".error_tip2")[0].style.display = "none";
        } else {
            $(".error_tip2")[0].innerHTML = "请勾选协议";
            $(".error_tip2")[0].style.display = "inline-block";
        }
    });


    //确定密码键盘某个键松开时提示
    $("[name='cpwd']").keyup(function () {
        if ($(this).val() === $("[name='pwd']").val()) {
            $(".error_tip")[2].style.display = "none";
        }
        else {
            $(".error_tip")[2].innerHTML = "密码不一致";
            $(".error_tip")[2].style.display = "inline-block";
        }
    });


    //密码失去光标时对密码进行正则验证
    $("[name='pwd']").blur(function () {
        if (18 >= $(this).val().length >= 6) {
            var regex = /^(\w){6,18}$/;
            var result = regex.test($(this).val());
            if (result) {
                $(".error_tip")[1].style.display = "none";
            } else {
                $(".error_tip")[1].innerHTML = "密码必须为6到18位字母、数字或下划线";
                $(".error_tip")[1].style.display = "inline-block";
            }
        }
        else if ($(this).val() === "") {
            $(".error_tip")[1].innerHTML = "密码不能为空";
            $(".error_tip")[1].style.display = "inline-block";
        }
        else if ($(this).val().length < 6 || $(this).val().length > 18) {
            $(".error_tip")[1].innerHTML = "密码长度必须为6到18位";
            $(".error_tip")[1].style.display = "inline-block";
        }
    });
    //确认密码失去光标时
    $("[name='cpwd']").blur(function () {
        if ($(this).val() === "") {
            $(".error_tip")[2].innerHTML = "请输入确认密码";
            $(".error_tip")[2].style.display = "inline-block";
        }
        else {
            $(".error_tip")[2].style.display = "none";
        }
    });
    //邮箱失去光标时对用户名进行正则验证
    $("[name='email']").blur(function () {
        var regex = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
        var result = regex.test($(this).val());
        if (result) {
            $(".error_tip")[3].style.display = "none";
        } else {
            $(".error_tip")[3].innerHTML = "请输入正确的邮箱格式";
            $(".error_tip")[3].style.display = "inline-block";
        }
    });

});