var test = new Vue({
    el: '#fileApp',
    delimiters: ['[[', ']]'],
    data: {
        directories: [],
        files: [],
        loader: true
    },
    mounted: async function () {
        var data = await $.getJSON('/api/file/list_item');
        this.files = data.file;
        this.directories = data.directory;
        this.loader = false
    },
    methods: {
        fileClicked: function (fileId, dirId) {
            window.open('/api/file/download?did=' + dirId + '&fid=' + fileId,'_blank');
        }
    }
});