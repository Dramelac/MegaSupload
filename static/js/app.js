async function loadDir(dirId, dirName) {
    this.loader = true;
    var data = await $.getJSON('/api/file/list_item?did=' + (dirId || ''));
    this.files = data.file;
    this.directories = data.directory.filter(function (d) {
        return d.name !== ".";
    }).sort(function (a, b) {
        return a - b;
    });
    this.loader = false;
    if (dirName === "..") {
        this.path.pop();
    } else if (dirName !== ".") {
        this.path.push(dirName + "/")
    }
    $("#path").text(this.path.join(""))
}
var fileManager = new Vue({
    el: '#fileApp',
    delimiters: ['[[', ']]'],
    data: {
        directories: [],
        files: [],
        loader: true,
        path: ["/"]
    },
    mounted: loadDir,
    methods: {
        fileClicked: function (fileId, dirId) {
            window.open('/api/file/download?did=' + dirId + '&fid=' + fileId,'_blank');
        },
        openDir: loadDir
    }
});