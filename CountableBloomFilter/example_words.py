def test(cbf):
    test_word(cbf, 'университет')
    test_word(cbf, 'итис')
    test_word(cbf, 'магистратура')
    test_word(cbf, 'сосна')
    test_word(cbf, 'кошка')
    test_word(cbf, 'сессия')
    test_word(cbf, 'крокодил')
    test_word(cbf, 'бакалавриат')
    test_word(cbf, 'а')
    test_word(cbf, 'студент')

def test_word(cbf, word):
    print(word + ' - ' + cbf.contains(word))
