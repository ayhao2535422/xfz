
function Index() {
    this.page = 2;
    this.category_id = 0;
}

Index.prototype.loadMoreClick = function(){
    var self = this;
    var loadMoreBtn = $('#load_more_btn');
    loadMoreBtn.click(function () {
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'p': self.page,
                'category_id': self.category_id
            },
            'success': function (result) {
                if (result['code'] === 0) {
                    var newses = result['data'];
                    if (newses.length > 0) {
                        var tpl = template('news_item', {'newses': newses})
                        var ul = $('.inner_news_box');
                        ul.append(tpl);
                        self.page++
                    }else {
                        loadMoreBtn.hide();
                    }
                }
            }
        })
    })
};

Index.prototype.categoryTabClick = function(){
    var self = this;
    var tabBox = $('.tab_box');
    tabBox.children('li').click(function () {
        var category_id = $(this).attr('data-category');
        $(this).addClass('active').siblings().removeClass('active')
        var page = 1;
        xfzajax.get({
            'url': '/news/list/',
            'data': {
                'category_id': category_id,
                'p': page
            },
            'success': function (result) {
                if (result['code'] === 0){
                    var newses = result['data'];
                    var ul = $('.inner_news_box');
                    var tpl = template('news_item', {'newses': newses});
                    ul.empty();
                    ul.append(tpl);
                    self.page = 2;
                    self.category_id = category_id

                }
            }
        })
    })
};

Index.prototype.run = function () {
    var self = this;
}

$(function () {
    var index = new Index();
    index.run();
})