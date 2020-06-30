function Banners() {

}

Banners.prototype.loadData = function(){
    var self = this;
    xfzajax.get({
        'url': '/cms/banner_list/',
        'success': function (result) {
            if (result['code'] === 200){
                var banners = result['data'];
                for (var i = 0; i < banners.length; i++) {
                    var banner = banners[i];
                    var tpl = template('banner_item', {'banner': banner});
                    var bannerListGroup = $('.banner_list_group');
                    bannerListGroup.append(tpl);
                    var bannerItem = bannerListGroup.find('.banner_item:last');
                    self.addImageSelectEvent(bannerItem);
                    self.removeBannerEvent(bannerItem);
                    self.saveBannerEvent(bannerItem);
                }
            }
        }
    })
};

Banners.prototype.listenAddBannerEvent = function(){
    var self = this;
    var addBtn = $('#add_banner_btn');


    addBtn.click(function () {
        var bannerListGroup = $('.banner_list_group');
        var bannerLength = bannerListGroup.children().length;
        if (bannerLength >= 6){
            window.messageBox.showInfo('最多只能添加6张轮播图');
            return;
        }else {
            var tpl = template('banner_item');
            bannerListGroup.prepend(tpl);
            var bannerItem = bannerListGroup.find('.banner_item:first');
            self.addImageSelectEvent(bannerItem);
            self.removeBannerEvent(bannerItem);
            self.saveBannerEvent(bannerItem);
        }
    })
};

Banners.prototype.addImageSelectEvent = function(bannerItem){
    var image = bannerItem.find('.thumbnail');
    var imageInput = bannerItem.find('.image_input');
    image.click(function () {
        imageInput.click();
    });
    imageInput.change(function () {
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
                    image.attr('src', url)
                }
            }
        });
    });
};

Banners.prototype.removeBannerEvent = function(bannerItem){
    var closeBtn = bannerItem.find('.close_btn');
    closeBtn.click(function () {
        var bannerId = bannerItem.attr('data-banner-id');
        if (bannerId){
            xfzalert.alertConfirm({
                'text': '确定要删除吗？',
                'confirmCallback': function () {
                    xfzajax.post({
                        'url': '/cms/del_banner/',
                        'data': {
                            'banner_id': bannerId
                        },
                        'success': function (result) {
                            if (result['code'] === 200){
                                window.location.reload();
                                window.messageBox.showSuccess('删除成功')
                            }
                        }
                    })
                }
            });
        }else {
            bannerItem.remove();
        }
    })
};

Banners.prototype.saveBannerEvent = function(bannerItem){
    var saveBtn = $('.save_btn');
    var imageTag = bannerItem.find('.thumbnail');
    var priorityTag = bannerItem.find("input[name='priority']");
    var link_toTag = bannerItem.find("input[name='link_to']");
    var prioritySpan = bannerItem.find('.priority');
    var bannerId = bannerItem.attr('data-banner-id');
    var url = '';
    if (bannerId){
        url = '/cms/edit_banner/';
    }else {
        url = '/cms/add_banner/';
    }
    saveBtn.click(function () {
        var image_url = imageTag.attr('src');
        var priority = priorityTag.val();
        var link_to = link_toTag.val();
        xfzajax.post({
            'url': url,
            'data': {
                'image_url': image_url,
                'priority': priority,
                'link_to': link_to,
                'pk': bannerId
            },
            'success': function (result) {
                if (result['code'] === 200){
                    if (bannerId){
                        window.messageBox.showSuccess('修改成功');
                    }else {
                        var bannerPk = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id', bannerPk);
                        window.messageBox.showSuccess('保存成功');
                    }
                    prioritySpan.text('优先级' + priority);
                }
            }
        })
    })
};

Banners.prototype.run = function () {
    var self = this;
    self.listenAddBannerEvent();
    self.loadData();
};

$(function () {
    var banners = new Banners();
    banners.run();
});