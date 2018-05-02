var currentDirId;

Vue.filter('prettyBytes', function (num) {
    if (!num) return 0;
    var i = Math.floor( Math.log(num) / Math.log(1024) );
    return ( num / Math.pow(1024, i) ).toFixed(2) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
});

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
    for (var key in iconClasses) {
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
    this.directories.map(function (d) {
        d.menuShown=null;
        return d;
    });
    this.loader = false;
    currentDirId = data.directory.find(function (d) {
        return d.type === "current";
    }).id;
    var curIndex = this.paths.findIndex(function (d) {
        return d.id === currentDirId;
    });
    if (curIndex > -1) {
        this.paths.length = curIndex + 1;
    } else {
        this.paths.push({
            name: dirName,
            id: currentDirId,
            show: !!dirId
        })
    }
}

function fileClicked(fileId) {
    var file = this.files.find(function (f) {
        return f.id == fileId;
    })
    var link = '/api/file/download?did=' + file.directory_id + '&fid=' + fileId;
    var el = document.createElement("i");
    el.className = "fas " + getFileIcon(file.type);
    if (/image/.test(file.type)) {
        el = new Image();
        el.src = link;
    } else if (/mp4/.test(file.type)) {
        el = newPLayer('video', link, file.type);
    } else if (/audio/.test(file.type)) {
        el = newPLayer('audio', link, file.type);
    } else if (/pdf/.test(file.type)) {
        el = document.createElement("iframe");
        el.src = link;
    }
    fileView.fileId = file.id;
    fileView.fileName = file.name;
    fileView.link = link;
    fileView.size = file.size;
    $('#fileDetailsModal .modal-body #fileContent').html(el);
    $("#fileDetailsModal").modal('show')
}
function mouseOver(dir){
    dir.menuShown = true;
    dir.name = dir.name + " ";
    console.log(dir.name + " over  "+ dir.menuShown);
    return dir.menuShown;
}
function mouseLeave(dir){
    dir.menuShown = false;
    dir.name = dir.name.trim(" ");
    console.log(dir.name + " leave "+ dir.menuShown);
    return dir.menuShown;
}
function newPLayer(playerType, src, mime) {
    var el = document.createElement(playerType);
    el.setAttribute('controls', true);
    el.setAttribute('autoplay', true);
    var source = document.createElement('source');
    source.setAttribute('src', src);
    source.setAttribute('type', mime);
    el.appendChild(source);
    return el;
}

function closeMenu() {
            this.viewMenu = false;
}

function openMenu(e) {
            this.viewMenu = true;

            Vue.nextTick(function() {
                this.$$.right.focus();
                console.log(e.y+"e x = "+e.x);
                this.top = e.y;
                this.left = e.x;
            }.bind(this));
            e.preventDefault();
}

var fileManager = new Vue({
    el: '#fileApp',
    delimiters: ['[[', ']]'],
    data: {
        directories: [],
        files: [],
        loader: true,
        paths: [],
        isOk : false,
        viewMenu: false,
        top: '0px',
        left: '0px'
    },
    mounted: loadDir,
    methods: {
        fileClicked: fileClicked,
        openDir: loadDir,
        getFileIcon: getFileIcon,
        mouseOver : mouseOver,
        mouseLeave : mouseLeave,
        openMenu: openMenu,
        closeMenu: closeMenu
    }
});

async function loadDataCounter() {
    var req = await $.getJSON('/api/user/ratio');
    this.dataUsed = req.dataUsed;
    this.maxDataAllowed = req.maxDataAllowed;
}


var dataCounter = new Vue({
    el: '#dataUsed',
    delimiters: ['[[', ']]'],
    data: {
        dataUsed: 0,
        maxDataAllowed: 0
    },
    mounted: loadDataCounter,
    methods: {
        loadDataCounter: loadDataCounter,
    }
});

var fileView = new Vue({
    el: '#fileDetailsModal',
    delimiters: ['[[', ']]'],
    data: {
        fileId: null,
        fileName: "",
        size: 0,
        link: ''
    }
});

$('#fileDetailsModal').on('hidden.bs.modal', function (e) {
    $('#fileDetailsModal .modal-body #fileContent').html('');
});

$('#uploadModal').on('hidden.bs.modal', function (e) {
    $('#uploadFileName').html('');
    $('#dropbox').removeClass("drapActive");
    $("#uploadInput").val("");
    $('#uploadProgress').hide()
});

$('#newDirModal').on('show.bs.modal', function (e) {
    $('#newDirName').val('');
});


$('#dropbox').on("dragenter", function (e) {
    e.preventDefault();
    $('#dropbox').addClass("drapActive");
});

$('#dropbox').on("dragleave", function (e) {
    e.preventDefault();
    $('#dropbox').removeClass("drapActive");
});
$(document).on("dragover", function (e) {
    e.preventDefault();
});
$(document).on("drop", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $('#dropbox').addClass("drapActive");
    var files = e.originalEvent.dataTransfer.files;
    $('#uploadFileName').text(files[0].name);
    $("#uploadInput").prop("files", files);
    $('#uploadModal').modal('show');
});

function progress(e) {
    if (e.lengthComputable) {
        var percentage = (e.loaded * 100) / e.total;
    }
}

$("#uploadBtn").on('click', async function () {
    var reqFileExist = await $.post('/api/file/check_file', JSON.stringify({
        'dirId': currentDirId,
        'fname': $("#uploadInput")[0].files[0].name
    }));
    $('#uploadProgress').val(0).show();
    var fileKeyDecrypted = "";
    if (reqFileExist.isFileExist) {
        var reqFileKey = await $.post('/api/file/get_key', JSON.stringify({
            'fileId': reqFileExist.fileId
        }));
        var privateKey = forge.pki.privateKeyFromPem(localStorage.priv_key);
        fileKeyDecrypted = privateKey.decrypt(forge.util.decode64(reqFileKey.key), 'RSA-OAEP');
    }
    var data = new FormData();
    data.append('file', $("#uploadInput")[0].files[0]);
    data.append('dirId', currentDirId);
    data.append('key', fileKeyDecrypted);
    $.ajax({
        type: 'POST',
        url: '/api/file/upload',
        data: data,
        xhr: function () {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                myXhr.upload.addEventListener('progress', function (e) {
                    if (e.lengthComputable) {
                        var percentage = (e.loaded * 100) / e.total;
                        $('#uploadProgress').val(percentage);
                    }
                }, false);
            }
            return myXhr;
        },
        cache: false,
        contentType: false,
        processData: false,

        success: function () {
            $('#uploadModal').modal('hide');
            fileManager.openDir(currentDirId);
            dataCounter.loadDataCounter();
        },

        error: function (err) {
            alert(err.responseJSON.message)
        }
    });
});

$('#newDirBtn').on('click', async function () {
    try {
        await $.post('/api/file/add_dir', JSON.stringify({
            name: $('#newDirName').val(),
            dirId: currentDirId
        }));
        $('#newDirModal').modal('hide');
        fileManager.openDir(currentDirId);
        dataCounter.loadDataCounter();
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$('#deleteFileBtn').on('click', async function () {
    if (!fileView.fileId || !confirm('Are you sure to delete file ?')) return;
    try {
        await $.post('/api/file/remove_file', JSON.stringify({
            fileId: fileView.fileId
        }));
        $('#fileDetailsModal').modal('hide');
        fileManager.openDir(currentDirId);
        dataCounter.loadDataCounter();
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$('#renameFileBtn').on('click', async function () {
    var newName = prompt('Enter new file name');
    if (!fileView.fileId || !newName) return;
    try {
        await $.post('/api/file/rename_file', JSON.stringify({
            fileId: fileView.fileId,
            name: newName
        }));
        $('#fileDetailsModal').modal('hide');
        fileManager.openDir(currentDirId);
        dataCounter.loadDataCounter();
    } catch (err) {
        alert(err.responseJSON.message);
    }
});
