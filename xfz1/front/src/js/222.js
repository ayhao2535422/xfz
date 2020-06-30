function Banners() {

}

Banners.prototype.loadBanner = function(){
    var self = this;
    xfzajax.get({
        'url': '/cms/banner_list/',
        'success': function (result) {
            if (result['code'] === 200){
                var banners = result['data'];
                for (var i = 0; i < banners.length; i++) {
                    var banner = banners[i];
                    var tpl = template('banner-item', {'banner': banner});
                    var bannerListGroup = $('.banner-list-group');
                    bannerListGroup.append(tpl);
                    var bannerItem = bannerListGroup.find(".banner-group:last");
                    bannerItem.attr('data-banner-id', banner.id);
                    self.imageSelect(bannerItem);
                    self.deleteBanner(bannerItem);
                    self.saveBanner(bannerItem);
                }
            }
        }
    })
};

Banners.prototype.addBannerEvent = function(){
    var self = this;
    var addBtn = $('#add-banner-btn');
    addBtn.click(function () {
        var tpl = template('banner-item');
        var bannerListGroup = $('.banner-list-group');
        var bannerItems = bannerListGroup.children();
        if (bannerItems.length > 5){
            window.messageBox.showError('最多只能添加6张轮播图');
        }else {
            bannerListGroup.prepend(tpl);
            var bannerItem = bannerListGroup.find('.banner-group:first');
            self.imageSelect(bannerItem);
            self.deleteBanner(bannerItem);
            self.saveBanner(bannerItem);
        }
    })
};

Banners.prototype.imageSelect = function(bannerItem){
    var self = this;
    var image = bannerItem.find("img[class=thumbnail]");
    var imageInput = image.siblings('input');
    image.click(function () {
        imageInput.click();
    });
    imageInput.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('file', file);
        xfzajax.post({
            'url': '/cms/upload_file/',
            'processData': false,
            'contentType': false,
            'data': formData,
            'success': function (result) {
                if (result['code'] === 200){
                    var url = result['data']['url'];
                    image.attr('src', url);
                }
            }
        })
    });
};

Banners.prototype.deleteBanner = function(bannerItem){
    var self = this;
    var closeBtn = bannerItem.find("#close-btn");
    closeBtn.click(function () {
        var bannerId = bannerItem.attr('data-banner-id');
        if (bannerId) {
            xfzalert.alertConfirm({
                'title': '确定要删除吗？',
                'confirmCallback': function () {
                    xfzajax.post({
                        'url': '/cms/del_banner/',
                        'data': {
                            'banner_id': bannerId
                        },
                        'success': function (result) {
                            if (result['code'] === 200){
                                bannerItem.remove();
                            }
                        }
                    })
                }
            })
        }else {
            bannerItem.remove();
        }
    });
};

Banners.prototype.saveBanner = function(bannerItem){
    var self = this;
    var saveBtn = bannerItem.find(".save_btn");
    saveBtn.click(function () {
        var prioritySpan = bannerItem.find("span[class='priority']");
        var bannerId = bannerItem.attr('data-banner-id');
        var priority = bannerItem.find("input[name='priority']").val();
        var image_url = bannerItem.find("img[class='thumbnail']").attr('src');
        var link_to = bannerItem.find("input[name='link_to']").val();
        if (bannerId){
            xfzajax.post({
                'url': '/cms/edit_banner/',
                'data': {
                    'pk': bannerId,
                    'priority': priority,
                    'image_url': image_url,
                    'link_to': link_to
                },
                'success': function (result) {
                    if (result['code'] === 200){
                        window.messageBox.showSuccess('修改成功');
                        prioritySpan.text('优先级：' + priority);
                    }
                }
            })
        } else {
            xfzajax.post({
                'url': '/cms/add_banner/',
                'data': {
                    'priority': priority,
                    'image_url': image_url,
                    'link_to': link_to
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        var bannerId = result['data']['banner_id'];
                        bannerItem.attr('data-banner-id', bannerId);
                        prioritySpan.text('优先级：' + priority);
                        window.messageBox.showSuccess('保存成功');
                    }
                }
            })
        }
    });
};

Banners.prototype.run = function () {
    var self = this;
    self.addBannerEvent();
    self.loadBanner();
};

$(function () {
    var banners = new Banners();
    banners.run();
});