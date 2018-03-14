function getFileIcon(mimeType) {
    var iconClasses = {
        'image': 'fa-file-image',
        'audio': 'fa-file-audio',
        'video': 'fa-file-video',
        'application/pdf': 'fa-file-pdf',
        'application/msword': 'fa-file-word',
        'application/vnd.ms-word': 'fa-file-word',
        'application/vnd.oasis.opendocument.text': 'fa-file-word',
        'application/vnd.openxmlformatsfficedocument.wordprocessingml': 'fa-file-word',
        'application/vnd.ms-excel': 'fa-file-excel',
        'application/vnd.openxmlformatsfficedocument.spreadsheetml': 'fa-file-excel',
        'application/vnd.oasis.opendocument.spreadsheet': 'fa-file-excel',
        'application/vnd.ms-powerpoint': 'fa-file-powerpoint',
        'application/vnd.openxmlformatsfficedocument.presentationml': 'fa-file-powerpoint',
        'application/vnd.oasis.opendocument.presentation': 'fa-file-powerpoint',
        'text/plain': 'fa-file-text',
        'text/html': 'fa-file-code',
        'application/json': 'fa-file-code',
        'application/gzip': 'fa-file-archive',
        'application/zip': 'fa-file-archive',
    };
    for(var key in iconClasses){
        if (new RegExp(key).test(mimeType)) {
            return iconClasses[key]
        }
    }
    return 'fa-file';
}

async function loadDir(dirId, dirName) {
    this.loader = true;
    this.files = [];
    this.directories = [];
    var data = await $.getJSON('/api/file/list_item?did=' + (dirId || ''));
    this.files = data.file;
    this.directories = data.directory.filter(function (d) {
        return d.name !== ".";
    }).sort(function (a, b) {
        return a - b;
    });
    this.loader = false;
    var curId = data.directory.find(function (d) {
        return d.type === "current";
    }).id;
    var curIndex = this.paths.findIndex(function (d) {
        return d.id === curId;
    });
    if (curIndex > -1) {
        this.paths.length = curIndex + 1;
    } else {
        this.paths.push({
            name: dirName,
            id: curId,
            show: !!dirId
        })
    }
}
var fileManager = new Vue({
    el: '#fileApp',
    delimiters: ['[[', ']]'],
    data: {
        directories: [],
        files: [],
        loader: true,
        paths: []
    },
    mounted: loadDir,
    methods: {
        fileClicked: function (fileId, dirId) {
            window.open('/api/file/download?did=' + dirId + '&fid=' + fileId,'_blank');
        },
        openDir: loadDir,
        getFileIcon: getFileIcon
    }
});