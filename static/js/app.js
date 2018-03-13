async function loadDir(dirId) {
    this.loader = true;
    var data = await $.getJSON('/api/file/list_item?did=' + (dirId || ''));
    this.files = data.file;
    this.directories = data.directory;
    this.loader = false;
    $("#path").text("/")
}
var fileManager = new Vue({
    el: '#fileApp',
    delimiters: ['[[', ']]'],
    data: {
        directories: [],
        files: [],
        loader: true
    },
    mounted: loadDir,
    methods: {
        fileClicked: function (fileId, dirId) {
            window.open('/api/file/download?did=' + dirId + '&fid=' + fileId,'_blank');
        },
        openDir: loadDir
    }
});