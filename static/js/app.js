var test = new Vue({
    el: '#fileApp',
    delimiters: ['[[', ']]'],
    data: {
        directories: [],
        files: []
    },
    mounted: async function () {
        var data = await $.getJSON('/api/file/list_item');
        this.files = data.file;
        this.directories = data.directory;
    }
});