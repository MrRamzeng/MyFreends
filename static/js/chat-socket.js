// document.querySelector('#users').onclick = function () {
//     $('#chats_list').hide()
//     $('#user_list').show()
// }
//
// document.querySelector('#chats').onclick = function () {
//     $('#user_list').hide()
//     $('#chats_list').show()
// }

// function handleFileSelectMulti(evt) {
//     var files = evt.target.files;
//     document.getElementById('preview_image').innerHTML = "";
//     for (var i = 0, f; f = files[i]; i++) {
//         var reader = new FileReader();
//
//         reader.onload = (function (theFile) {
//             return function (e) {
//                 var span = document.createElement('span');
//                 span.innerHTML = ['<img id="', escape(theFile.name),
//                     '" class="img-thumbnail" src="', e.target.result, '">'].join('');
//                 document.getElementById('preview_image').insertBefore(span, null);
//             };
//         })(f);
//         reader.readAsDataURL(f);
//     }
// }
//
// document.getElementById('chat_photo_input').addEventListener('change', handleFileSelectMulti, false);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// send message or image
function sendMessage(chatSocket, imgId) {
    var messageInputDom = document.querySelector('#chat_message_input');
    var message = messageInputDom.value;
    if (document.querySelector('#chat_message_input').value != '' || document.querySelector('#chat_photo_input').value != '') {
        chatSocket.send(JSON.stringify({
            'command': 'new_message',
            'message': message,
            'chat': chat_id,
            'author': userId,
            'imgId': imgId,
        }));
    }
    messageInputDom.value = '';
    // $('#chat_photo_input').val('');
    // $('#messagebox_container #preview_image').empty();
}

function displayingMessage() {
    var chatSocket = new ReconnectingWebSocket(
        'ws://' + window.location.host +
        '/ws/chat/' + chat_id + '/'
    );

    chatSocket.onopen = function (e) {
        fetchMessages();
    }

    // send smile image
    // document.querySelector('#smile_list').onclick = function (e) {
    //     var smile = e.target.id;
    //     chatSocket.send(JSON.stringify({
    //         'command': 'new_message',
    //         'chat': chat_id,
    //         'author': userId,
    //         'smileId': smile,
    //     }));
    // };

    chatSocket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        if (data['command'] === 'messages') {
            for (let i = 0; i < data['messages'].length; i++) {
                createMessage(data['messages'][i]);
            }
        } else if (data['command'] === 'new_message') {
            createMessage(data['message']);
        }
    };

    chatSocket.onclose = function (e) {
        $('#messages').empty();
    };

    document.querySelector('#chat_message_input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#message_submit').click();
        }
    };

    document.querySelector('#message_submit').onclick = function (e) {
        e.stopPropagation();
        e.preventDefault()
        // var files = $('#chat_photo_input')[0].files[0]
        // if (files) {
        //     var fd = new FormData();
        //     fd.append('img', files);
        //     $.ajax({
        //         url: uploadImageUrl,
        //         type: "POST",
        //         cache: false,
        //         processData: false,
        //         contentType: false,
        //         data: fd,
        //         success: function (data) {
        //             sendMessage(chatSocket, data.id);
        //         }
        //     });
        // } else {
        sendMessage(chatSocket);
        // }
        $(document).ready(function () {
            $('#messages').scrollTop(9999)
        });
    };

    function fetchMessages() {
        chatSocket.send(JSON.stringify({'command': 'fetch_messages'}));
    }

    function createMessage(data) {
        var author = data['author'];
        var msgListTag = document.createElement('li');
        var userContainer = document.createElement('div');
        userContainer.className = 'chat-avatar';
        var authorImgTag = document.createElement('img');
        authorImgTag.src = data['author_image'];
        var authorTag = document.createElement('div');
        authorTag.className = 'chat-name';
        authorTag.textContent = data['author_fname'];
        var text = document.createElement('div');
        text.className = 'chat-text';
        text.textContent = data['content']
        userContainer.appendChild(authorImgTag);
        userContainer.appendChild(authorTag)
        if (author == userId) {
            msgListTag.appendChild(userContainer);
            msgListTag.appendChild(text);
            msgListTag.className = 'chat-left';
        } else {
            msgListTag.appendChild(text);
            msgListTag.appendChild(userContainer);
            msgListTag.className = 'chat-right';
        }
        document.querySelector('#messages').appendChild(msgListTag);


        //     if (data.img) {
        //         var file = document.createElement('img');
        //         file.setAttribute('src', data.img)
        //         file.setAttribute('class', 'message-img')
        //         if (data.message) {
        //         }
        //         pTag.appendChild(file)
        //     }
        //     if (data.smile) {
        //         var file = document.createElement("img");
        //         file.setAttribute('src', data.smile)
        //         file.setAttribute('class', 'smile')
        //         pTag.appendChild(file)
        //     }
        $(document).ready(function () {
            $('#messages').scrollTop(9999)
        });
    }
}

hash = window.location.hash

function displayingForm() {
    $('#current_user').empty()
    $('#' + chat_id).clone().appendTo("#current_user")
    $('.chat-container').show().css('display', 'flex')
    displayingMessage()
}

function selectingForm() {
    $(".users a").click(function (event) {
        chat_id = (event.target.id)
        $('.person').removeClass('active-user')
        if ($('#' + chat_id).parent('a').attr('href') != window.location.hash) {
            $('li#' + chat_id).addClass('active-user')
            $('#messages').empty()
            displayingForm()
        }
    });
}

$(window).bind('hashchange', function () {
    if (window.location.hash != '') {
        $('.chat-container').show().addClass('d-flex')
    } else {
        $('.chat-container').hide()
    }
});

if (window.location.hash != '') {
    chat_id = (hash.slice(1))
    displayingForm()
    $('li#' + chat_id).addClass('active-user')
    selectingForm()
} else {
    selectingForm()
}
