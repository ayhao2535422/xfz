
function FrontBase() {

}

FrontBase.prototype.hover = function () {
    var authorBox = $(".author_box");
    var moreBox = $(".user_more_box");
    authorBox.hover(function () {
        moreBox.show();
    }, function () {
        moreBox.hide();
    })
};

FrontBase.prototype.navClick = function(){
    var url = window.location.href;
    var protocol = window.location.protocol;
    var host = window.location.host;
    var domain = protocol + '//' + host
    var path = url.replace(domain, '');
    var lis = $('.list_box li');
    lis.each(function (index, element) {
        var li = $(element);
        var a = li.children('a');
        var href = a.attr('href');
        if (href === path){
            li.addClass('active').siblings().removeClass('active')

        }
    })
};


FrontBase.prototype.run = function () {
    var self = this;
    self.hover();
    self.navClick();
};


$(function () {
    var front_base = new FrontBase();
    front_base.run()

});


function Auth() {
    this.signinBtn = $("#signin");
    this.signupBtn = $("#signup");
    this.closeBtn = $(".close_btn");
    this.maskBox = $(".mask_box");
    this.rightSpan = $(".right_span");
    this.rightSpan1 = $(".right_span1");
    this.authDiv = $(".auth-2_div");
}

Auth.prototype.click = function(){
    var self = this;
    self.signinBtn.click(function () {
        self.maskBox.show();
        self.authDiv.css({"left":0})
    });
    self.closeBtn.click(function () {
        self.maskBox.hide();
    });
    self.rightSpan.click(function () {
        self.authDiv.animate({"left":-400});
    });
    self.rightSpan1.click(function () {
        self.authDiv.animate({"left":0})
    });

    self.signupBtn.click(function () {
        self.maskBox.show();
        self.authDiv.css({"left":-400})
    })
};

Auth.prototype.smsCaptchaClick = function(){
    var self = this;
    var smsCaptcha = $('.send_captcha');
    var signupDiv = $('.signup_div');
    smsCaptcha.click(function () {
        var telephoneInput = signupDiv.find("input[name='telephone']");
        var telephone = telephoneInput.val();
        if (!telephone){
            window.messageBox.showInfo('请输入手机号码')
        }
        xfzajax.get({
            'url': '/account/sms_captcha/',
            'data': {
                'telephone': telephone
            },
            'success': function (result) {
                if (result['code'] === 200){
                    window.messageBox.showSuccess('短信验证码发送成功');
                    smsCaptcha.unbind('click');
                    smsCaptcha.addClass('disabled');
                    var count = 10;
                    var timer = setInterval(function () {
                        smsCaptcha.val(count + 's');
                        count -= 1;
                        if (count < 0){
                            clearInterval(timer);
                            smsCaptcha.removeClass('disabled');
                            smsCaptcha.val('发送验证码');
                            self.smsCaptchaClick();
                        }
                    },1000)
                }
            }
        })
    })
};

Auth.prototype.captchaClick = function(){
    var self = this;
    var captcha = $('.captcha');
    captcha.click(function () {
        captcha.attr('src', '/account/captcha/'+ '?random=' + Math.random())
    })
};

Auth.prototype.signinEvent = function(){
    var self = this;
    var signinDiv = $(".signin_div");
    var signinTelephone = signinDiv.find("input[name='telephone']");
    var signinPassword = signinDiv.find("input[name='password']");
    var signinRemember = signinDiv.find("input[name='remember']");
    var signinSubmit = signinDiv.find(".submit");

    signinSubmit.click(function () {
        var telephone = signinTelephone.val();
        var password = signinPassword.val();
        var remember = signinRemember.prop("checked");

        xfzajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember?1:0
            },
            'success': function (result) {
                console.log(result);
                if (result['code'] === 200){
                    self.maskBox.hide();
                    window.location.reload();
                    var message = result['message'];
                    if (typeof message == 'string' || message.constructor == String){
                        window.messageBox.show(message)
                    }
                    else {
                        for (var key in message){
                            var first = message[key][0];
                            window.messageBox.show(first)
                        }
                    }
                }
                else {}
            },
            'fail': function (error) {
                console.log(error)
            }
        })
    })
};

Auth.prototype.signupEvent = function(){
    var self = this;
    var signupDiv = $('.signup_div');
    var submit1 = signupDiv.find("input[class='submit1']");

    submit1.click(function () {
        var signupTelephone = signupDiv.find("input[name='telephone']");
        var signupUsername = signupDiv.find("input[name='username']");
        var signupPassword = signupDiv.find("input[name='password']");
        var signupPassword1 = signupDiv.find("input[name='password1']");
        var signupImgCaptcha = signupDiv.find("input[name='img_captcha']");
        var signupSmsCaptcha = signupDiv.find("input[name='sms_captcha']");

        var telephone = signupTelephone.val();
        var username = signupUsername.val();
        var password = signupPassword.val();
        var password1 = signupPassword1.val();
        var imgCaptcha = signupImgCaptcha.val();
        var smsCaptcha = signupSmsCaptcha.val();
        xfzajax.post({
            'url': '/account/register/',
            'data': {
                'telephone': telephone,
                'username': username,
                'password': password,
                'password1': password1,
                'img_captcha': imgCaptcha,
                'sms_captcha': smsCaptcha
            },
            'success': function () {
                window.messageBox.showSuccess('注册成功');
                window.location.reload()
            }
        })
    })
};

Auth.prototype.run = function(){
    var self = this;
    self.click();
    self.signinEvent();
    self.signupEvent();
    self.captchaClick();
    self.smsCaptchaClick();
};

$(function () {
    var auth = new Auth();
    auth.run();
});

$(function () {
    if (window.template) {
        template.defaults.imports.timeSince = function (dateValue) {
            var date = new Date(dateValue);
            var datets = date.getTime();
            var nowts = (new Date()).getTime();
            var timestamp = (nowts - datets) / 1000;
            if (timestamp < 60) {
                return '刚刚';
            } else if (timestamp >= 60 && timestamp < 60 * 60) {
                minute = parseInt(timestamp / 60);
                return minute + '分钟前';
            } else if (timestamp >= 60 * 60 && timestamp < 60 * 60 * 24) {
                hour = parseInt(timestamp / 60 / 60);
                return hour + '小时前';
            } else if (timestamp >= 60 * 60 * 24 && timestamp < 60 * 60 * 24 * 30) {
                day = parseInt(timestamp / 60 / 60 / 24);
                return day + '天前';
            } else {
                var year = date.getFullYear();
                var month = date.getMonth();
                var day = date.getDay();
                var hour = date.getHours();
                var minute = date.getMinutes();
                return year + '/' + month + '/' + day + ' ' + hour + ':' + minute
            }
        }
    }
});