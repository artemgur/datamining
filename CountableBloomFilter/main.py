import cbf_creator
import database

words = database.get_words()
cbf = cbf_creator.create_optimal(0.0001, 4000)
for word in words:
    cbf.add(word)
print(cbf.get_false_positive_probability())
while True:
    word = input()
    print(cbf.contains(word))