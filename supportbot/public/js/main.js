var chat = {
	mode: null,
	start: 0,
	last_message_from_user: null,
	last_message_from_bot: null,
	handle: function() {
		if(chat.last_message_from_user) {
			chat.get_answer()
		} else {
			chat.add_comment('Go ahead, type something', true);
		}
	},
	get_answer: function(query, callback) {
		chat.last_question = chat.last_message_from_user;
		$.ajax({
			url: '/api/method/supportbot.api.get_answer',
			data: {
				question: chat.last_message_from_user,
				start: chat.start
			},
			dataType: 'json',
			success: function(r) {
				if(r.message) {
					chat.add_comment('I found this:\n\n' + markdown(r.message), true);
					chat.add_comment('Was this useful?', true);
					chat.add_option([
						{
							label: 'Yes',
							action: function() {
								chat.start = 0;
							}
						},
						{
							label: 'No',
							action: function() {
								// get another answer
								chat.start++;
								chat.last_message_from_user = chat.last_question;
								chat.get_answer();
							}
						}
					]);
				} else {
					chat.add_comment('Sorry could not find anything for that query. Ask something else?', true);
				}
			}
		})
	},
	add_comment: function(html, from_bot) {
		// save the last comment
		if(from_bot) {
			chat.last_message_from_bot = html;
		} else {
			chat.last_message_from_user = html;
		}

		// display it
		$('<div class="commentArea bubbled'+ (from_bot ? 'Left' : 'Right')
			+'"></div>').prependTo('.answers').html(html);
	},
	add_option: function(options) {
		var div  = $('<div>').prependTo('.answers');
		options.forEach(function(o) {
			var option = $('<span class="commentArea bubbledOption"></span>')
				.appendTo(div)
				.html(o.label)
				.attr('data-value', o.label)
				.on('click', function() {
					chat.add_comment($(this).attr('data-value'));
					$(this).parent().remove();
					$('.question').prop('disabled', false);

					// do the action
					$(this).get(0).action();
				});

				// attach the action to this object so
				// so it can be called on click
				option.get(0).action = o.action;
		});
		$('.question').prop('disabled', true);
	}
}

$(document).ready(function() {
	$('.question').on('keydown', function(e) {
		if(e.which==13) { // && (e.ctrlKey || e.metaKey)) {
			chat.add_comment($(this).val());
			$(this).val('');
			chat.handle();
			return false;
		};
	});
	chat.mode = 'question';
	chat.add_comment('Hello, I am Umair and can help you get started with ERPNext. Ask me a question', true)
});

var markdown = function(txt) {
	if(!window.md2html) {
		window.md2html = new Showdown.converter();
	}

	while(txt.substr(0,1)==="\n") {
		txt = txt.substr(1);
	}

	// remove leading tab (if they exist in the first line)
	var whitespace_len = 0,
		first_line = txt.split("\n")[0];

	while([" ", "\n", "\t"].indexOf(first_line.substr(0,1))!== -1) {
		whitespace_len++;
		first_line = first_line.substr(1);
	}

	if(whitespace_len && whitespace_len != first_line.length) {
		var txt1 = [];
		$.each(txt.split("\n"), function(i, t) {
			txt1.push(t.substr(whitespace_len));
		})
		txt = txt1.join("\n");
	}

	return window.md2html.makeHtml(txt);
}
