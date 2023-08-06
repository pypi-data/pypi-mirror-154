def Persian(text, P=False):
    #persian character to arabic and vise versa,
    #to set a standard between tsetmc and my program;
	if P:
		# Arabic 2 Persian 
		Text = text.replace('ي','ی')
		Text = Text.replace('ك','ک')
	else:
		# Persian 2 Arabic
		Text = text.replace('ک', 'ك')
		Text = Text.replace('ی', 'ي')

	return Text