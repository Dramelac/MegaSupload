var currentDirId;

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
    if (/image\/|mp4|audio\//.test(file.type)) {
        if (/image/.test(file.type)) {
            var el = new Image();
            el.src = link;
        } else if (/mp4/.test(file.type)) {
            var el = newPLayer('video', link, file.type);
        } else if (/audio/.test(file.type)) {
            var el = newPLayer('audio', link, file.type);
        }
        $("#globalModal .modal-title").text(file.name)
        $('#globalModal .modal-body').html(el);
        $("#globalModal").modal('show')
    } else {
        window.open(link, '_blank');
    }
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
        paths: []
    },
    mounted: loadDir,
    methods: {
        fileClicked: fileClicked,
        openDir: loadDir,
        getFileIcon: getFileIcon
    }
});

$('#globalModal').on('hidden.bs.modal', function (e) {
    $('#globalModal .modal-body').html('');
});

$('#uploadModal').on('hidden.bs.modal', function (e) {
    $('#uploadFileName').html('');
    $('#dropbox').removeClass("drapActive");
    $("#uploadInput").val("");
    $('#uploadProgress').hide()
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
            fileManager.openDir(currentDirId)
        },

        error: function (err) {
            console.log(err);
            alert(err.responseText || err)
        }
    });
});

$('#newDirBtn').on('click', async function () {
    try {
        await $.post('/api/file/add_dir', JSON.stringify({
            name: $('#newDirName').val(),
            dirId: currentDirId
        }))
        $('#newDirModal').modal('hide');
        fileManager.openDir(currentDirId)
    } catch (err) {
        alert("Error on folder creation");
    }
});
