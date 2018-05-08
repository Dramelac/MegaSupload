var currentDirId;

Vue.filter('prettyBytes', function (num) {
    if (!num) return 0;
    var i = Math.floor(Math.log(num) / Math.log(1024));
    return (num / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
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

async function loadDir(dirId, dirName, event) {
    if (typeof event !== 'undefined' && (event.target.tagName === 'BUTTON' || event.target.tagName === 'A')) return;
    this.loader = true;
    this.files = [];
    this.directories = [];
    if ($('#toggleShare').attr('aria-pressed') === "true") {
        var data = await $.getJSON('/api/share/ls');
    } else {
        var data = await $.getJSON('/api/file/list_item?did=' + (dirId || ''));
    }

    this.files = data.file.map(function (f) {
        f.link = '/api/file/download?did=' + f.directory_id + '&fid=' + f.id;
        f.menuShown = false;
        return f;
    });
    this.directories = data.directory.filter(function (d) {
        return d.name !== ".";
    }).map(function (d) {
        d.menuShown = false;
        return d;
    }).sort(function (a, b) {
        return a - b;
    });
    this.loader = false;
    if ($('#toggleShare').attr('aria-pressed') === "true") {
        currentDirId = null;
        this.paths = []
    } else {
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
}

function fileClicked(fileId, event) {
    if (typeof event !== 'undefined' && (event.target.tagName === 'BUTTON' || event.target.tagName === 'A')) return;
    var file = this.files.find(function (f) {
        return f.id == fileId;
    })
    var el = document.createElement("i");
    el.className = "fas " + getFileIcon(file.type);
    if (/image/.test(file.type)) {
        el = new Image();
        el.src = file.link
    } else if (/mp4/.test(file.type)) {
        el = newPLayer('video', file.link, file.type);
    } else if (/audio/.test(file.type)) {
        el = newPLayer('audio', file.link, file.type);
    } else if (/pdf/.test(file.type)) {
        el = document.createElement("iframe");
        el.src = file.link;
    }
    fileView.file = file;
    $('#fileDetailsModal .modal-body #fileContent').html(el);
    $("#fileDetailsModal").modal('show')
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


var fileManager = new Vue({
    el: '#fileApp',
    delimiters: ['[[', ']]'],
    data: {
        directories: [],
        files: [],
        loader: true,
        paths: [],
        isOk: false,
        viewMenu: false,
        top: '0px',
        left: '0px'
    },
    mounted: loadDir,
    methods: {
        fileClicked: fileClicked,
        openDir: loadDir,
        getFileIcon: getFileIcon
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
        file: {
            id: null,
            name: "",
            size: 0,
            link: '',
        },
        searchIsActive: false,
        searchUserResults: [],
        userSelected: {
            id: null,
            name: null
        }
    },
    methods: {
        resetSearch: function() {
            this.searchIsActive = false;
            this.searchUserResults = [];
            this.userSelected = {
                id: null,
                name: null
            };
        }
    }
});

$('#fileDetailsModal').on('hidden.bs.modal', function (e) {
    $('#fileDetailsModal .modal-body #fileContent').html('');
    fileView.resetSearch();
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
    if (reqFileExist.isFileExist && localStorage.priv_key) {
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

$('#toggleShare').on('click', function () {
    setTimeout(function () {
        if ($('#toggleShare').attr('aria-pressed') === "true") {
            $('.notForShare').hide()
        } else {
            $('.notForShare').show()
        }
        fileManager.openDir();
    });
});

$(document).on('click', '.deleteBtn', async function () {
    var id = $(this).attr('data-id');
    var type = $(this).attr('data-type');
    if (!id || !type || !confirm('Are you sure to delete ' + type +' ?')) return;
    try {
        await $.post('/api/file/remove_' + type, JSON.stringify({
            id: id
        }));
        $('#fileDetailsModal').modal('hide');
        fileManager.openDir(currentDirId);
        dataCounter.loadDataCounter();
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$(document).on('click', '.renameBtn', async function () {
    var type = $(this).attr('data-type');
    var newName = prompt('Enter new  ' + type + ' name');
    var id = $(this).attr('data-id');
    if (!id || !type || !newName) return;
    try {
        await $.post('/api/file/rename_' + type, JSON.stringify({
            id: id,
            name: newName
        }));
        $('#fileDetailsModal').modal('hide');
        fileManager.openDir(currentDirId);
        dataCounter.loadDataCounter();
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$(document).on('input', '#searchUserInput', async function () {
    fileView.userSelected = {
        id: null,
        name: null
    };
    var val = $(this).val();
    if (!fileView.file.id) return;
    var data = await $.getJSON('/api/user/search?query=' + val);
    fileView.searchUserResults = data.results
});

$(document).on('click', '.searchUserDiv', function () {
    fileView.searchUserResults = [];
    fileView.userSelected.id = $(this).attr('data-userid');
    fileView.userSelected.name = $(this).attr('data-name');
});
$(document).on('click', '#submitShareBtn', async function () {
    try {
        var res = await $.post('/api/share/share', JSON.stringify({
            'elementId': fileView.file.id,
            'targetUserId': fileView.userSelected.id,
            'encryptedKey': 'TODO',
            'read': 1,
            'write': $('#writePerm').is(":checked"),
            'share': $('#sharePerm').is(":checked")
        }));
        fileView.resetSearch();
        alert(res.message)
    } catch (e) {
        alert(e.responseJSON.message)
    }
});

