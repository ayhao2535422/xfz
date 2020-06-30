
function CourseDetail() {

}

CourseDetail.prototype.initPlayer = function () {
    var videoInfoSpan = $('#video-info');
    var videoUrl = videoInfoSpan.attr('data-video-url');
    var coverUrl = videoInfoSpan.attr('data-cover-url');
    var player = cyberplayer("playercontainer").setup({
        width: '100%',
        height: '100%',
        file: videoUrl,
        image: coverUrl,
        autostart: false,
        stretching: "uniform",
        repeat: false,
        volume: 100,
        controls: true,
        tokenEncrypt: true,
        // AccessKey
        ak: 'fa2c9444fd024eb2a790985caeabc30a'
    });

    player.on('beforePlay', function (e) {
        if (!/m3u8/.test(e.file)) {
            return;
        }
        xfzajax.get({
            // 获取token的url
            'url': '/course/course_token/',
            'data': {
                'video': videoUrl
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token'];
                    player.setToken(e.file, token);
                } else {
                    alert('token错误！');
                }
            },
            'fail': function (error) {
                console.log(error);
            }
        });
    });
};

CourseDetail.prototype.run = function () {
    var self = this;
    self.initPlayer();
}

$(function () {
    var courseDetail = new CourseDetail();
    courseDetail.run();
})