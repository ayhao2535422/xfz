
function TeacherList() {

}

TeacherList.prototype.addTeacher = function(){
    var addBtn = $('.add-teacher');
    addBtn.click(function () {
        xfzajax.post({
            'url': ''
        })
    })
};

TeacherList.prototype.run = function () {
    var self = this;
}

$(function () {
    var teacher = new TeacherList();
    teacher.run();
})