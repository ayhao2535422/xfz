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
                    var messageObject = result['message'];
                    if (typeof messageObject == 'string' || messageObject.constructor == String){
                        window.messageBox.show(messageObject);
                    }
                    else {
                        for (var key in messageObject){
                            var message = message[key][0];
                            window.messageBox.show(message)
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

Auth.prototype.run = function(){
    var self = this;
    self.click();
    self.signinEvent();
};

$(function () {
    var auth = new Auth();
    auth.run();
});