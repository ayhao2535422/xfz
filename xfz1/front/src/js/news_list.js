
function CmsNewsList() {

}

CmsNewsList.prototype.initDatePicker = function () {
    var startPicker = $("#start-picker");
    var endPicker = $("#end-picker");

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth()+1) + '/' + todayDate.getDate();
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

CmsNewsList.prototype.deleteBtnEvent = function(){
    var delBtn = $('.del-btn');
    delBtn.click(function () {
        var news_id = $(this).attr('data-news-id')
        xfzalert.alertConfirm({
            'title': '确定要删除吗？',
            'confirmCallback': function (value) {
                xfzajax.post({
                    'url': '/cms/delete_news/',
                    'data': {
                        'news_id': news_id
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            window.location.reload();
                        }
                    }
                })
            }
        })
    })
};

CmsNewsList.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.deleteBtnEvent();
};

$(function () {
    var newsList = new CmsNewsList();
    newsList.run();
});