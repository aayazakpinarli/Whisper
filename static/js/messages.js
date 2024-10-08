let input_message = $('#input-message')
let input_file = document.getElementById('input-file');
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()

let loc = window.location
let wsStart = 'wss://'
let endpoint = wsStart + loc.host + loc.pathname

var socket = new WebSocket(endpoint)

socket.onopen = async function(e) {
    console.log('open', e)
    send_message_form.on('submit', function(e){
        e.preventDefault();
        let message = input_message.val()
        let file = input_file.files[0]
        console.log('message', message)
        console.log('file', file)
        // base64 stringinin başında data:image yazıyo
        // checks the image or not
        if (message && !message.includes('data:')) {
            let send_to = get_active_other_user_id();
            let thread_id = get_active_thread_id();
            let data = {
                'message': message,
                'sent_by': USER_ID,
                'send_to': send_to,
                'thread_id': thread_id
            }
            data = JSON.stringify(data)
            socket.send(data)
            $(this)[0].reset()
        }
        if (file) {
            getBase64(file).then(
                (res) => {
                    let send_to = get_active_other_user_id();
                    let thread_id = get_active_thread_id();
                    let data = {
                        'message': res,
                        'sent_by': USER_ID,
                        'send_to': send_to,
                        'thread_id': thread_id
                    }
                    data = JSON.stringify(data)
                    socket.send(data)
                    $(this)[0].reset()
                }
            )
        }
    })
}

socket.onmessage = async function(e) {
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    newMessage(message, sent_by_id, thread_id)
}

socket.onerror = async function(e) {
    console.log('error', e)
}

socket.onclose = async function(e) {
    console.log('close', e)
}

function newMessage(message, sent_by_id, thread_id) {
	if ($.trim(message) === '') {
		return false;
	}
    let time = new Date();
    let timestamp = time.getDate() + ' ' + time.getDay() + ', ' + time.getHours() + ':' +time.getMinutes();

	let message_element;
	let chat_id = 'chat_' + thread_id
	if(sent_by_id == USER_ID){
        if (message.includes('data:image')) {
            message_element = `
			<div class="d-flex mb-4 replied">
				<div class="msg_cotainer_send">
                    <a href="${message}" download="image.png">
                        <img src="${message}" style="max-width: 150px; max-height: 100px;"></img>
                    </a>
					<span class="msg_time_send">${timestamp}</span>
				</div>
				<div class="img_cont_msg">
					<img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
				</div>
			</div>
	        `
        } else {
            message_element = `
			<div class="d-flex mb-4 replied">
				<div class="msg_cotainer_send">
					${message}
					<span class="msg_time_send">${timestamp}</span>
				</div>
				<div class="img_cont_msg">
					<img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
				</div>
			</div>
	        `
        }
    }
	else{
        if (message.includes('data:image')) {
            message_element = `
            <div class="d-flex mb-4 received">
                <div class="img_cont_msg">
                    <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
                </div>
                <div class="msg_cotainer">
                    <a href="${message}" download="image.png">
                        <img src="${message}" style="max-width: 150px; max-height: 100px;"></img>
                    </a>
                <span class="msg_time">${timestamp}</span>
                </div>
            </div>
            `
        } else {
            message_element = `
            <div class="d-flex mb-4 received">
                <div class="img_cont_msg">
                    <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg" class="rounded-circle user_img_msg">
                </div>
                <div class="msg_cotainer">
                    ${message}
                <span class="msg_time">${timestamp}</span>
                </div>
            </div>
            `
        }
    }

    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .msg_card_body')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);
}

$('.contact-li').on('click', function (){
    $('.contacts .active').removeClass('active')
    $(this).addClass('active')

    // message wrappers
    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active')

})

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    let thread_id = chat_id.replace('chat_', '')
    return thread_id
}

function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
}