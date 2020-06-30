function NewsCategory() {

}

NewsCategory.prototype.click = function(){
    var self = this;
    var addBtn = $('#add_btn');
    addBtn.click(function () {
        xfzalert.alertOneInput({
            'title': '新闻分类',
            'placeholder': '请输入分类',
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/add_category/',
                    'data': {
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200){
                            window.location.reload();
                        }else {
                            xfzalert.close();
                        }
                    }
                })
            }
        })
    });

    var editBtn = $('.edit_btn');
    editBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        var name = tr.attr('data-name');
        xfzalert.alertOneInput({
            'title': '分类',
            'text': '请输入新的分类名称',
            'value': name,
            'confirmCallback': function (inputValue) {
                xfzajax.post({
                    'url': '/cms/edit_category/',
                    'data': {
                        'pk': pk,
                        'name': inputValue
                    },
                    'success': function (result) {
                        if (result['code'] === 200){
                            window.location.reload();
                        }else {
                            window.xfzalert.close();
                        }
                    }
                })
            }
        })
    });

    var delBtn = $('.delete_btn');
    delBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr('data-pk');
        xfzalert.alertConfirm({
            'title': '您确定要删除吗',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/cms/del_category/',
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

NewsCategory.prototype.run = function () {
    var self = this;
    self.click();
};

$(function () {
    var category = new NewsCategory();
    category.run();
});