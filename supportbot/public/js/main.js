var chat = 
{
	mode: null,
	start: 0,
	iter: 0,
	last_message_from_user: null,
	last_message_from_bot: null,
	fit1: 0,
	name1: null,
	handle: function() 
	{
		if(chat.mode == 'question')
		{
			console.log('Handling your question')
			if(chat.last_message_from_user) 
				chat.get_answer()
			else 
				chat.add_comment('Go ahead, type something', true);	
		}

		else if(chat.mode == 'neural_net')
		{
			if(chat.last_message_from_user)
				chat.neural_net()
			else
				chat.add_comment('Go ahead, type something', true);
		}

		else if(chat.mode == 'fitness')
		{
			if(chat.last_message_from_user)
			{
				chat.fit1 = parseInt(chat.last_message_from_user)
				if((chat.fit1<0) || (chat.fit1>10))
					chat.add_comment('Please enter a legible value in the range (0, 10)', true);
				else
					chat.set_fitness()
			}
			else
			{
				chat.mode = 'question';
				chat.add_comment('Oh..so you dont want to give a rating!\n Thats OK!\n Tell us.. what more do you want to know?', true)
			}
		}
		
	},

	neural_net: function()
	{
		chat.last_question = chat.last_message_from_user;	
		$.ajax(
		{
			url: '/api/method/supportbot.neural_net.answer',
			data:
			{
				question: chat.last_question,
				i: chat.iter
			},
			dataType: 'json',
			success: function(r)
			{
				if(r.message) 
				{
					chat.name1 = r.message.name;
					console.log(chat.name1)
					//console.log(r.message.r)
					chat.add_comment('I found this:\n\n' + markdown(r.message.raw), true);
					chat.add_comment('Do you want another answer?', true);
					chat.add_option(
					[
						{
							label: 'Yes',
							action: function() 
							{
								// get another answer
								chat.iter++;
								chat.last_message_from_user = chat.last_question;
								chat.neural_net();
							}
						},
						{
							label: 'No',
							action: function() 
							{
								chat.add_comment('Cool!\n So ask us something more..', true)
								chat.iter = 0;
							}
						}
					]);					
				} 
				else 
					chat.add_comment('Sorry could not find anything for that query. Ask something else?', true);	
			}
		})
	},

	set_fitness: function()
	{
		$.ajax(
		{
			url: '/api/method/supportbot.api.set_fitness',
			data:
			{
				_fit: chat.fit1,
				name: chat.name1	
			},
			dataType: 'json',
			success: function()
			{	
				chat.mode = 'question'
				chat.add_comment('Thank you for the review.\n Do you want another answer?', true);
				chat.add_option(
				[
					{
						label: 'Yes',
						action: function() 
						{
							// get another answer
							chat.start++;
							chat.last_message_from_user = chat.last_question;
							chat.get_answer();
						}
					},
					{
						label: 'No',
						action: function() 
						{
							chat.add_comment('Cool!\n So ask us something more..', true)
							chat.start = 0;
						}
					}
				]);
			}
			
		})
	},

	get_answer: function() 
	{
		console.log('In get_answer function')
		chat.last_question = chat.last_message_from_user;
		$.ajax(
		{
			url: '/api/method/supportbot.api.get_answer',
			data: 
			{
				question: chat.last_message_from_user,
				start: chat.start
			},
			dataType: 'json',
			success: function(r) 
			{
				if(r.message) 
				{
					chat.name1 = r.message.name;
					console.log(chat.name1)
					chat.add_comment('I found this:\n\n' + markdown(r.message.raw), true);
					chat.mode = 'fitness';
					chat.add_comment('Would you like to rate this answer on a scale of 0 to 10?', true);
				} 
				else 
					chat.add_comment('Sorry could not find anything for that query. Ask something else?', true);
			}
		})
	},

	add_comment: function(html, from_bot) 
	{
		console.log('adding comment')
		// save the last comment
		if(from_bot)
		{
			console.log('setting up last_message_from_bot') 
			chat.last_message_from_bot = html;
		}
		else 
		{
			console.log('setting up last_message_from_user')
			chat.last_message_from_user = html;
		}
			

		// display it
		$('<div class="commentArea bubbled'+ (from_bot ? 'Left' : 'Right')
			+'"></div>').prependTo('.answers').html(html);
	},

	add_option: function(options) 
	{
		var div  = $('<div>').prependTo('.answers');
		options.forEach(function(o) 
		{
			var option = $('<span class="commentArea bubbledOption"></span>')
				.appendTo(div)
				.html(o.label)
				.attr('data-value', o.label)
				.on('click', function() 
				{
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

$(document).ready(function() 
{
	$('.question').on('keydown', function(e) 
	{
		if(e.which==13) 
		{ // && (e.ctrlKey || e.metaKey)) {
			chat.add_comment($(this).val());
			$(this).val('');
			chat.handle();
			return false;
		};
	});

	console.log('Started successfully!')
	chat.mode = 'confused';
	chat.add_comment('Are you a trainer or user?', true);
	chat.add_option(
				[
					{
						label: 'Trainer',
						action: function() 
						{
							chat.mode = 'question'
							chat.add_comment('Hi!, Come, Help us train this bot for ERPNext. Ask me a question', true);
						}
					},
					{
						label: 'User',
						action: function() 
						{
							chat.mode = 'neural_net'
							chat.add_comment('Hello, I am Umair and can help you get started with ERPNext. Ask me a question', true);
						}
					}
				]);
});

var markdown = function(txt) 
{
	if(!window.md2html) 
		window.md2html = new Showdown.converter();

	while(txt.substr(0,1)==="\n") 
		txt = txt.substr(1);

	// remove leading tab (if they exist in the first line)
	var whitespace_len = 0,
		first_line = txt.split("\n")[0];

	while([" ", "\n", "\t"].indexOf(first_line.substr(0,1))!== -1) 
		whitespace_len++;
		first_line = first_line.substr(1);

	if(whitespace_len && whitespace_len != first_line.length) 
	{
		var txt1 = [];
		$.each(txt.split("\n"), function(i, t) 
		{
			txt1.push(t.substr(whitespace_len));
		})
		txt = txt1.join("\n");
	}

	return window.md2html.makeHtml(txt);
}