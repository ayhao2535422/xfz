function PublishNews() {

}

PublishNews.prototype.initUEditor = function(){
    var self = this;
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/'
    });
};

PublishNews.prototype.change = function(){
    var self = this;
    var thumbnailBtn = $('#thumbnail_btn');
    thumbnailBtn.change(function () {
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
                    var thumbnailForm = $('#thumbnail-form');
                    thumbnailForm.val(url);
                }
            }
        })
    })
};

PublishNews.prototype.listenQiniuUploadEvent = function(){
    var self = this;
    var thumbnailBtn = $('#thumbnail_btn');
    thumbnailBtn.change(function () {
        var file = this.files[0];
        xfzajax.get({
            'url': '/cms/qiniutoken/',
            'success': function (result) {
                if (result['code'] === 200){
                    var token = result['data']['token'];
                    var key = (new Date().getTime() + '.' + file.name.split('.')[1]);
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpeg', 'image/gif']
                    };
                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z2
                    };
                    var observable = qiniu.upload(file, key, token, putExtra, config);
                    observable.subscribe({
                        'next': self.handlerUploadProgress,
                        'error': self.handlerUploadError,
                        'complete': self.handlerUploadComplete
                    });
                }
            }
        })
    })
};

PublishNews.prototype.handlerUploadComplete = function(response){
    var progressGroup = $('#progress-group');
    var progressBar = $('.progress-bar');
    var thumbnailInput = $('#thumbnail-form');
    var domain = 'http://qa7m1cg3t.bkt.clouddn.com/';
    var fileName = response['key'];
    var url = domain + fileName;
    progressGroup.hide();
    progressBar.css({'width': 0});
    thumbnailInput.val(url);
};

PublishNews.prototype.handlerUploadError = function(error){
    window.messageBox.showError(error.message);
    console.log(error.message);
};

PublishNews.prototype.handlerUploadProgress = function(response){
    var total = response.total;
    var percent = total.percent;
    var progressGroup = $('#progress-group');
    progressGroup.show();
    var progressBar = $('.progress-bar');
    progressBar.css({'width': percent.toFixed(0) + '%'});
    progressBar.text(percent.toFixed(0) + '%');
};

PublishNews.prototype.listenSubmitEvent = function(){
    var self = this;
    var submitBtn = $('#submit_btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        var title = $("input[name='title']").val();
        var category = $("select[name='category']").val();
        var desc = $("input[name='desc']").val();
        var thumbnail = $("input[name='thumbnail']").val();
        var content = window.ue.getContent();
        var pk = submitBtn.attr('data-news-id');
        var url = '';
        if (pk){
            url = '/cms/edit_news/'
        }else {
            url = '/cms/publish/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content,
                'pk': pk
            },
            'success': function (result) {
                if (result['code'] === 200){
                    xfzalert.alertSuccess('新闻发布成功！', function f() {
                        window.location.reload();
                    });
                }
            }
        })
    })
};

PublishNews.prototype.run = function () {
    var self = this;
    self.listenQiniuUploadEvent();
    self.initUEditor();
    self.listenSubmitEvent();
    self.change();
};

$(function () {
    var publish = new PublishNews();
    publish.run();
});