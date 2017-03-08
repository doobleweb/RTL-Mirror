import sublime
import sublime_plugin
import re
#this function show the hebrew word Correctly
#in sublime text the word show at reverse.
#the program start by click on the button "ALT+ A"
class rtlMirrorCommand(sublime_plugin.TextCommand):

	settings = sublime.load_settings("RTL-Mirror.sublime-settings")
	
	SPACE_WORD=" " # a character that divide between words
	VALEU_BETWEEN_SELECTION = settings.get("VALEU_BETWEEN_SELECTION") #This character causes the separation between each selection
	VALEU_BETWEEN_WORD= "<br>"# a character that divide between the word in display

	#This function accepts the position of the selected word and converts it to the word itself
	#This function creates an array with all the selection the user  and shows the Hebrew words in the right type.

	def run(self,edit): 
		view=self.view
		sels = view.sel() # def array that return a selection value
		# select_word_arr=[] # a first array that include the selection and show it in array.
		count_word=0 #this character help to put a max word in line
		first_array=[] #the first array that all word enter to this array , and after 6 words the array append to second arr and reset 
		ready_aray=[] # the second arr , the final arr that contain all value to show for user
		count_selection=0

	
		for point_word in sels: 
			without_space=view.substr(view.word(point_word)).split(self.WORD_DEVIDER) 
			count_word=0 
			count_selection=count_selection+1
			first_array=[]

			for str_word in without_space :
				str_word=str_word.strip("")	
				str_word=str_word.replace("\n","")

				if(count_word==self.SETTINGS.get("words_per_line")):
					first_array.reverse()
					ready_aray.append(self.WORD_DEVIDER.join(first_array))
					ready_aray.append(self.LINE_DEVIDER)
					first_array = [];
					count_word=0
				else:
					count_word=count_word+1

				first_array.append(self.revers_start_end_word(str_word))

			self.put_br(sels, count_selection,ready_aray,first_array)
		self.show_pop(ready_aray)

	#this function put a br and character between the selection
	def put_br(self, sels,count_selection ,ready_aray,first_array ):
		first_array.reverse()
		ready_aray.append(self.WORD_DEVIDER.join(first_array))
		if(count_selection<len(sels)):
				ready_aray.append(self.LINE_DEVIDER)
				ready_aray.append(self.SELECTION_DEVIDER) # enter the character in final selection
				ready_aray.append(self.LINE_DEVIDER)

	#this function show the selection in pop_up
	def show_pop(self, arr):
		select_word_arr=[] # a first array that include the selection and show it in array.
		divide_with_space=self.WORD_DEVIDER.join(arr) #create a string with word and put a space between the word
		select_word_arr.append(divide_with_space) # enter the word(string) to array 
		show_a_string=self.LINE_DEVIDER.join(select_word_arr) #create a string with all words because a function-popup identify only string
		self.view.show_popup(show_a_string, max_width=self.SETTINGS.get("window_max_width")) #Shows a popup displaying HTML content.


	#this function give a solution in case that have a character (not alphanomeric)
	def revers_start_end_word(self,word):
		first_char=""
		last_char=""
		counter=0
		word=word.strip("")	
		char_in_word =re.sub(self.ALL_CHARS_AND_DIGITS_REGEX, "", word)
		while (counter<(len(word))):
			if (len(word)== len(char_in_word)):
				return char_in_word[::-1]
			counter=counter+1
			if (word[0] in char_in_word):
				first_char=word[0]+first_char
				word=list(word)
				del(word[0])
				counter= counter-1
				word="".join(word) 
			if (word[-1] in char_in_word):
				last_char=last_char+word[-1]
				print("last char" + last_char)
				word=list(word)
				del(word[-1])
				counter= counter-1
				word="".join(word)

		last_char[::-1]
		first_char[::-1]
		return last_char + word +first_char
