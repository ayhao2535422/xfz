
function CourseList() {

}

CourseList.prototype.initDatePicker = function () {
    var startPicker = $("#start-picker");
    var endPicker = $("#end-picker");

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth() + 1) + '/' + todayDate.getDate();
    var options = {
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2017/6/1',
        'endDate': todayStr,
        'language': 'zh-CN',
        'todayBtn': 'linked',
        'todayHighlight': true,
        'clearBtn': true,
        'autoclose': true
    };
    startPicker.datepicker(options);
    endPicker.datepicker(options);
};

CourseList.prototype.editBtnClick = function(){
    var editBtn = $('.edit-btn');
    editBtn.click(function () {
        var pk = $(this).attr('data-id');
        xfzajax.get({
            'url': '/cms/edit_course/',
            'data': {
                'pk': pk
            },
            'success': function (result) {
                if (result['code'] === 200){

                }
            }
        })
    })
};

CourseList.prototype.run = function () {
    var self = this;
    self.initDatePicker();
}

$(function () {
    var course = new CourseList();
    course.run();
})