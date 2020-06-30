function NewsList() {

}

NewsList.prototype.listenSubmitEvent = function(){
    var self = this;
    var submitBtn = $('.submit_btn');
    var textarea = $("textarea[name='comment']");
    submitBtn.click(function () {
        var content = textarea.val();
        var news_id =submitBtn.attr('data-news_id');
        xfzajax.post({
            'url': '/news/public_comment/',
            'data': {
                'content': content,
                'news_id': news_id
            },
            'success': function (result) {
                if (result['code'] === 200){
                    var comment = result['data'];
                    var tpl = template('comment_item', {'comment': comment});
                    var commentList = $('.comment_list');
                    commentList.prepend(tpl);
                    window.messageBox.showSuccess('评论成功');
                    textarea.empty();
                }
            }
        })
    })
};

NewsList.prototype.run = function () {
    var self = this;
    self.listenSubmitEvent();
};

$(function () {
    var newsList = new NewsList();
    newsList.run();
});