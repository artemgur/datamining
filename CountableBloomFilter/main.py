import cbf_creator
import database
import example_words

words = database.get_words()
cbf = cbf_creator.create_optimal(0.00001, 6000) #One extra 0 to precision, because the count of elements is imprecise
for word in words:
    cbf.add(word)
print(cbf.get_false_positive_probability())
example_words.test(cbf)