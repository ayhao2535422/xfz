
function CourseCategory() {

}

CourseCategory.prototype.addCategory = function(){
    var addBtn = $('.add-btn');
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title': '请输入分类名',
            'confirmCallback': function (value) {
                xfzajax.post({
                    'url': '/cms/add_course_category/',
                    'data': {
                        'category': value
                    },
                    'success': function (result) {
                        if (result['code'] === 200){
                            window.location.reload();
                        }
                    }
                })
            }
        })
    })
};

CourseCategory.prototype.editCategory = function(){
    var editBtn = $('.edit-btn');
    editBtn.click(function () {
        var pk = $(this).attr('data-id')
        console.log(pk)
        xfzalert.alertOneInput({
            'title': '编辑分类',
            'confirmCallback': function (value) {
                xfzajax.post({
                    'url': '/cms/edit_course_category/',
                    'data': {
                        'pk': pk,
                        'name': value
                    },
                    'success': function (result) {
                        if (result['code'] === 200){
                            window.location.reload();
                        }
                    }
                })
            }
        })
    })
};

CourseCategory.prototype.delCategory = function(){
    var delBtn = $('.del-btn');
    delBtn.click(function () {
        var pk = $(this).attr('data-id')
        xfzalert.alertConfirm({
            'title': '确定要删除吗？',
            'confirmCallback': function (value) {
                xfzajax.post({
                    'url': '/cms/del_course_category/',
                    'data': {
                        'pk': pk
                    },
                    'success': function (result) {
                        if (result['code'] === 200){
                            window.location.reload();
                        }
                    }
                })
            }
        })
    })
};

CourseCategory.prototype.run = function () {
    var self = this;
    self.addCategory();
    self.editCategory();
    self.delCategory();
};

$(function () {
    var course = new CourseCategory();
    course.run();
})