from collections import Counter
import re
class tf_idf:
	def __init__(self, text):
		self.text = text
		self.table_tf = ""

	def get_df(self):
		n = [x for x in self.text.lower().replace(" ", "-").split("-") if x != ""]
		freq_words = [list(x) for x in [(x, y) for (x, y) in Counter(n).items()]]
		tf = [i.append(i[1] / len(n)) for i in freq_words]
		return freq_words

	
my_text = "The car    is driven  on the   road"
print(tf_idf(my_text).get_df())
