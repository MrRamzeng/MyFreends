// document.querySelector('#users').onclick = function () {
//     $('#chats_list').hide()
//     $('#user_list').show()
// }
//
// document.querySelector('#chats').onclick = function () {
//     $('#user_list').hide()
//     $('#chats_list').show()
// }

function handleFileSelectMulti(evt) {
    var files = evt.target.files;
    document.getElementById('preview_image').innerHTML = "";
    for (var i = 0, f; f = files[i]; i++) {
        var reader = new FileReader();

        reader.onload = (function (theFile) {
            return function (e) {
                const image = document.createElement('img');
                $(image).attr('id', escape(theFile.name));
                $(image).attr('class', 'img-thumbnail');
                $(image).attr('src', e.target.result);
                $('#preview_image').append(image);
            };
        })(f);
        reader.readAsDataURL(f);
    }
}

document.getElementById('image-input').addEventListener('change', handleFileSelectMulti, false);

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
    if (
        document.querySelector('#chat_message_input').value != '' ||
        document.querySelector('#image-input').value != ''
    ) {
        chatSocket.send(JSON.stringify({
            'command': 'new_message',
            'message': message,
            'chat': chat_id,
            'author': userId,
            'imgId': imgId,
        }));
    }
    messageInputDom.value = '';
    $('#image-input').val('');
    $('#chat-box #preview_image').empty();
}

function displayingMessage() {
    var wsProto = window.location.protocol === "https:" ? "wss" : "ws";
    var chatSocket = new ReconnectingWebSocket(wsProto + '://' + window.location.host + '/ws/chat/' + chat_id + '/');

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
        if (data.command === 'count') {
            $('.badge').text(data.counter)
        }
        if (data.command === 'messages') {
            let length = data.messages.length;
            for (let i = 0; i < length; i++) {
                createMessage(data.messages[i]);
            }
            if (data.messages) {
                markAsRead(data.messages[length - 1].id, currentUser);
            }
        } else if (data.command === 'new_message') {
            createMessage(data.message);
            if (data.command === 'count') {
                $('.badge').text(data.counter)
            }
            if (data.message.author != userId) {
                markAsRead(data.message.id, currentUser);
                if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|BB|PlayBook|IEMobile|Windows Phone|Kindle|Silk|Opera Mini/i.test(navigator.userAgent)) {
                    $('.toast strong').text(data.message.author_full_name);
                    $('.toast img').attr('src', data.message.author_image);
                    if (data.message.img) {
                        $('.toast-body strong').text('Изображение. ' + data.message.content)
                    } else {
                        $('.toast-body strong').text(data.message.content);
                    }
                    $('.toast').toast({'delay': 3000});
                    $('.toast').toast('show');
                }
                var myAudio = new Audio;
                myAudio.src = audioSrc;
                myAudio.play();
            }
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
        var files = $('#image-input')[0].files[0]
        if (files) {
            var fd = new FormData();
            fd.append('img', files);
            $.ajax({
                url: uploadImageUrl,
                type: "POST",
                cache: false,
                processData: false,
                contentType: false,
                data: fd,
                success: function (data) {
                    sendMessage(chatSocket, data.id);
                }
            });
        } else {
            sendMessage(chatSocket);
        }
        $(document).ready(function () {
            $('#messages').scrollTop(9999)
        });
    };

    function fetchMessages() {
        chatSocket.send(JSON.stringify({'command': 'fetch_messages'}));
    }

    function createMessage(data) {
        var messageContent = document.createElement('div');
        $(messageContent).attr('class', 'message-content');
        $(messageContent).append(data.content);

        var clockContainer = document.createElement('h5');

        var authorFullName = document.createElement('h4');
        $(authorFullName).append(data.author_full_name);

        var divider = document.createElement('hr');

        var infoContainer = document.createElement('div');
        $(infoContainer).attr('class', 'info-container');

        var authorImage = document.createElement('img');
        $(authorImage).attr('src', data.author_image);

        var messageContainer = document.createElement('div');
        $(messageContainer).attr('class', 'message-container');

        var imageContainer = document.createElement('div');
        $(imageContainer).attr('class', 'image-container');
        $(imageContainer).append(authorImage);

        var authorContainer = document.createElement('li');

        $(clockContainer).append(data.timestamp);

        $(infoContainer).append(authorFullName);
        $(infoContainer).append(clockContainer);

        $(messageContainer).append(infoContainer);
        $(messageContainer).append(divider);
        $(messageContainer).append(messageContent);
        if (data.author == userId) {
            $(authorContainer).attr('class', 'sender-container');
            $(authorContainer).append(messageContainer);
            $(authorContainer).append(imageContainer);
        } else {
            $(authorContainer).attr('class', 'recipient-container');
            $(authorContainer).append(imageContainer);
            $(authorContainer).append(messageContainer);
        }
        document.querySelector('#messages').appendChild(authorContainer);


        if (data.img) {
            var file = document.createElement('img');
            $(file).attr({'src': data.img, 'class': 'message-img'})
            if (data.message) {
            }
            $(messageContent).append(file)
        }
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

    function markAsRead(messageId, currentUser) {
        chatSocket.send(JSON.stringify({
            'command': 'read_message',
            'message_id': messageId,
            'currentUser': currentUser,
        }))
    }
}

hash = window.location.hash

function displayingForm() {
    $('.chat-container').show().css('display', 'flex')
    displayingMessage()
}

function selectingForm() {
    $(".users a").click(function (event) {
        chat_id = (event.target.id)
        $('.person').removeClass('active-user')
        if ($('#' + chat_id).parent('a').attr('href') != window.location.hash) {
            $('li#' + chat_id).addClass('active-user')
            $('li .badge').remove()
            $('#messages').empty()
            displayingForm()
            window.location.hash = chat_id;
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
