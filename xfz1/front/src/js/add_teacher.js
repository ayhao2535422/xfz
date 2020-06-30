
function AddTeacher() {

}

AddTeacher.prototype.initUEditor = function(){
    window.ue = UE.getEditor('editor', {
        'serverUrl': '/ueditor/upload/'
    })
};

AddTeacher.prototype.uploadEvent = function(){
    var uploadBtn = $('#avatar-btn');
    uploadBtn.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200){
                    var url = result['data']['url'];
                    $("input[name='avatar']").val(url)
                }
            }
        })
    })
};

AddTeacher.prototype.submitEvent = function(){
    var submitBtn = $('.submit-btn');
    submitBtn.click(function () {
        var username = $("input[name='username']").val();
        var jobtitle = $("input[name='jobtitle']").val();
        var avatar = $("input[name='avatar']").val();
        var profile = ue.getContent();

        xfzajax.post({
            'url': '/cms/add_teacher/',
            'data': {
                'username': username,
                'jobtitle': jobtitle,
                'avatar': avatar,
                'profile': profile
            },
            'success': function (result) {
                if (result['code'] === 200){
                    window.xfzalert.alertSuccess('添加成功')
                    window.location.reload();
                }
            }
        })
    })
};

AddTeacher.prototype.run = function () {
    var self = this;
    self.initUEditor();
    self.uploadEvent();
    self.submitEvent();
}

$(function () {
    var teacher = new AddTeacher();
    teacher.run();
})