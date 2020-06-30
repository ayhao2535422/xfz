
function PubCourse() {

}

PubCourse.prototype.initUEditor = function () {
    window.ue = UE.getEditor("editor",{
        'serverUrl': '/ueditor/upload/'
    });
};

PubCourse.prototype.submitClick = function(){
    var submitBtn = $('#submit-btn');
    submitBtn.click(function () {
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var teacher = $("select[name='teacher']").val();
        var video_url = $("input[name='video']").val();
        var cover_url = $("input[name='cover']").val();
        var price = $("input[name='price']").val();
        var duration = $("input[name='duration']").val();
        var profile = window.ue.getContent();

        xfzajax.post({
            'url': '/cms/publish_course/',
            'data': {
                'title': title,
                'video_url': video_url,
                'cover_url': cover_url,
                'price': price,
                'duration': duration,
                'profile': profile,
                'category': category,
                'teacher': teacher
            },
            'success': function (result) {
                if (result['code'] === 200){
                    window.location.reload();
                }
            }
        })
    })
};

PubCourse.prototype.run = function () {
    var self = this;
    self.initUEditor();
    self.submitClick();
}

$(function () {
    var course = new PubCourse();
    course.run();
})