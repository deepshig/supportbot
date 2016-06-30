var chat = 
{
	mode: null,
	start: 0,
	iter: 0,
	last_message_from_user: null,
	last_message_from_bot: null,
	fit1: 0,
	name1: null,
	isans:0,
	session1: 0,
	uname1: null,
	country1: null,
	email_id1: null,
	domain1: null,
	feedback1: null,

	getRandomInt: function() 
	{
    	return Math.floor(Math.random() * (10000000 + 1));
	},

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
				console.log(chat.fit1)
				if((chat.fit1<0) || (chat.fit1>10))
					chat.add_comment('Please enter a legible value in the range (0, 10)', true);
				else
					chat.set_fitness()
			}
			else
			{
				chat.add_comment('Oh..so you dont want to give a rating!\n Thats OK!\n Tell us.. Do you want to know something else?', true)
				chat.ques_or_intro();
			}
		}

		else if(chat.mode == 'intro_name')
		{
			if(chat.last_message_from_user)
			{
				chat.uname1 = chat.last_message_from_user;
				chat.mode = 'intro_country'
				chat.add_comment('Thats a nice name! \n Which country are you from?', true);
			}
			else
				chat.add_comment('Come On.. Dont be shy now!!', true)
		}

		else if(chat.mode == 'intro_country')
		{
			if(chat.last_message_from_user)
			{
				chat.country1 = chat.last_message_from_user;
				chat.mode = 'intro_domain'
				chat.add_comment('Hmm...So what domain do you work in?', true);
			}
			else
				chat.add_comment("Dont worry, we are not going to send terrorists there! \n Tell us..", true);
		}

		else if(chat.mode == 'intro_domain')
		{
			if(chat.last_message_from_user)
			{
				chat.domain1 = chat.last_message_from_user;
				chat.mode = 'intro_feedback'
				chat.add_comment('Thats cool!!! \n Do you wish to suggest us some feedback?', true);
			}
			else
				chat.add_comment("Dont be silly now! \n Thats not something to hide", true);
		}

		else if(chat.mode == 'intro_feedback')
		{
			if(chat.last_message_from_user)
			{
				chat.feedback1 = chat.last_message_from_user;
				chat.mode = 'intro_email'
				chat.add_comment('Thank You! \n We will surely work towards the betterment of our product. \n Lastly, can we have your email id?', true)
			}
			else
				chat.add_comment('Please do share your thoughts. Feel free.. We value suggestions form our customers.', true);
		}

		else if(chat.mode == 'intro_email')
		{
			if(chat.last_message_from_user)
			{
				chat.email_id1 = chat.last_message_from_user;
				chat.mode = 'feed_details'
				chat.feed_detail()
				chat.add_comment('Thank You. \n Do ping us the next time you are in need')
			}
			else
				chat.add_comment('Trust us.. We wont spam you!', true)
		}
		
	},

	feed_detail: function()
	{
		$.ajax(
		{
			url: '/api/method/supportbot.api.feed_detail',
			data:
			{
				unam: chat.uname1,
				email: chat.email_id1,
				cntry: chat.country1,
				dmn: chat.domain1,
				fb: chat.feedback1,
			},
			dataType: 'json',
			success: function()
			{
				chat.add_comment('Thank You for all the interaction. We have stored your details. We will contact you whenever there is an update regarding your domain of work', true)
				chat.mode = 'confused'
				chat.add_comment('You have ended this session. \n Please reload the page to start a new session.', true)
			}
		})
	},

	ques_or_intro: function()
	{	
		chat.add_option(
		[
			{
				label: 'Yes',
				action: function() 
				{
					if(chat.mode == 'fitness' || chat.mode == 'question')
						chat.mode = 'question';
					else
						chat.mode = 'neural_net';

					chat.add_comment('Cool!\n Ask us more..', true)
					chat.iter = 0;
				}
			},
			{
				label: 'No',
				action: function() 
				{
					chat.add_comment('It was nice talking to you :D \n Would you like to tell us a bit about yourself?', true)
					chat.intro();
				}
			}
		]);	
	},

	intro: function()
	{
		chat.add_option(
		[
			{
				label: 'Yes',
				action: function() 
				{
					chat.mode = 'intro_name'
					chat.add_comment('So.. Whats your name?', true)
				}
			},
			{
				label: 'No',
				action: function() 
				{
					chat.add_comment('Thats fine..seems you are bored!! \n Not a problem.. ping us the next time you are in need..', true)
				}
			}
		]);	
	},

	neural_net: function()
	{
		console.log('in neural_net function - main.js')
		console.log(chat.iter)
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
					chat.isans = 1;
					chat.add_comment('I found this:\n\n' + markdown(r.message.raw), true);
					
					chat.add_comment('Do you want another answer for this question?', true);
					chat.isoption = 1;
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
								chat.iter = 0;
								chat.add_comment('Oh.. Okay.. Do you want to know something else?', true)
								chat.ques_or_intro();
							}
						}
					]);					
				} 
				else 
				{
					chat.add_comment('Sorry could not find anything for that query. Do you wish to ask something else?', true);
					chat.ques_or_intro();
				}	
			}
		})
	},

	set_log: function(message, from_bot)
	{
		// console.log('In set_log function - main.js')
		$.ajax(
		{
			url: '/api/method/supportbot.api.set_log',
			data:
			{
				msg: message,
				bot: from_bot,
				session: chat.session1
			},	
			dataType: 'json',
			success: function()
			{
				chat.isans = 0;
			}
		})
		// console.log('Done with set_log function - main.js')
	},

	set_fitness: function()
	{
		console.log(chat.fit1)
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
				chat.add_comment('Thank you for the review.\n Do you want another answer for this question?', true);
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
							chat.start = 0;
							chat.add_comment('Thats Okay!! \n Do you want to know something else?', true)
							chat.ques_or_intro();							
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
				{
					chat.add_comment('Sorry could not find anything for that query. Do you wish to ask something else?', true);
					chat.ques_or_intro()
				}
			}
		})
	},

	add_comment: function(html, from_bot) 
	{
		console.log('adding comment')
		// save the last comment
		if(chat.mode == 'neural_net' && chat.session1!=0)
		{
			if(from_bot)
				bot = 1
			else
				bot = 0
			if(chat.isans==1)
			{
				chat.set_log(chat.name1, bot);
				chat.isans = 0;
			}
			else
				chat.set_log(html, bot)
		}
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
	chat.session1 = chat.getRandomInt();
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
							//chat.set_log('User', 0);
							//chat.set_log('Hello, I am Umair and can help you get started with ERPNext. Ask me a question', 1)
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

	while([" ", "\n", "\t"].indexOf(first_line.substr(0,1)) != -1)
	{
		whitespace_len++;
		first_line = first_line.substr(1);
	} 

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