
function CourseIndex() {

}

CourseIndex.prototype.listenSwitchEvent = function(){
    var self = this;
    var ul = $('.nav_ul');
    ul.children('li').click(function () {
        var li = $(this);
        var pk = li.attr('data-pk');
        xfzajax.get({
            'url': '/course/course_list/',
            'data': {
                'pk': pk
            },
            'success': function (result) {
                if (result['code'] === 200){
                    var courses = result['data']
                    var tpl = template('course-item',{'courses': courses})
                    var course_ul = $('.course_ul');
                    course_ul.empty();
                    course_ul.append(tpl);
                    li.addClass('active').siblings().removeClass('active')
                }
            }
        })
    })
};

CourseIndex.prototype.run = function () {
    var self = this;
    self.listenSwitchEvent();
}

$(function () {
    var course = new CourseIndex();
    course.run();
})