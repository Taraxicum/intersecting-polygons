from filters import OrderingFilter, RepeatedStepFilter, MaxFullLengthStepFilter, HappyPathFilter, Lemma1Filter, ParityFilter,SimpleParityFilter

def test_ordering_filter():
    print("testing ordering filter")
    f = OrderingFilter(5)
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 2, 4, 3]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 5, 3]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 3, 5, 2]])
    assert f.apply_filter([[2, 3, 4], [1, 3, 5, 2]])
    assert f.apply_filter([[2, 3], [1, 3, 5, 2]])
    assert not f.apply_filter([[1, 3, 4], [1, 3, 5, 2]])

def test_repeated_step_filter():
    print("testing repeated step filter")
    f = RepeatedStepFilter(5)
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 4, 3]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 3, 5, 2], [1, 2, 3, 4]])
    assert not f.apply_filter([[2, 3, 4], [2, 3, 4, 5]])
    assert f.apply_filter([[2, 3], [1, 3, 5, 2], [2, 3]])

def test_max_full_length_step_filter():
    print("testing max full length step filter")
    f = MaxFullLengthStepFilter(5)
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]) 
    assert f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4], [2, 3], [1, 2, 3, 4], [1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2], [2, 3], [3, 4], [1, 4], [1, 4]])

def test_happy_path_filter():
    f = HappyPathFilter(5)
    assert not f.apply_filter([])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3]])
    assert f.apply_filter([[1, 2]])
    assert f.apply_filter([[1, 2], [1, 2, 3]])
    assert f.apply_filter([[1, 2], [2, 3]])
    assert not f.apply_filter([[1, 2, 3, 4], [2, 3, 4], [1, 2, 3, 5]])
    assert f.apply_filter([[1, 2, 3, 4], [2, 3, 4], [1, 2, 3, 5], [4, 3, 5]])

def test_lemma_1_filter():
    print("testing Lemma 1 filter")
    f = Lemma1Filter(5)
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]) 
    assert f.apply_filter([[1,2,3,4,5,6,7,8],[9,2,3,4,5,6,7,8],[1,4,3,2,5,8,7,6]])
    assert not f.apply_filter([[1,2,3,4,5,6,7,8],[9,2,3,4,5,6,7,8],[8,7,6,1,5,2,4,3]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4], [2, 3], [1, 2, 3, 4], [1, 2, 3, 4]])

def test_parity_filter():
    print("testing parity filter")
    f = ParityFilter(9)
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert f.apply_filter([[1, 3, 2, 4]])
    assert not f.apply_filter([[1, 2, 3, 5, 6]])
    assert f.apply_filter([[1, 3, 2, 5, 6, 7]])
    assert f.apply_filter([[1, 2, 3, 5, 7, 6]])
    assert not f.apply_filter([[8, 9, 1]]), "should allow valid parity wrt wrapping"
    assert f.apply_filter([[8, 9, 2, 1]]), "should filter invalid parity wrt wrapping" # not currently implemented so this test is failing

def test_simple_parity_filter():
    print("testing simple parity filter")
    f = SimpleParityFilter(9)
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert f.apply_filter([[1, 3, 2, 4]])
    assert not f.apply_filter([[1, 2, 3, 5, 6]])
    assert f.apply_filter([[1, 3, 2, 5, 6, 7]])
    assert f.apply_filter([[1, 2, 3, 5, 7, 6]])
    assert not f.apply_filter([[8, 9, 1]]), "should allow valid parity wrt wrapping"
    assert f.apply_filter([[8, 9, 2, 1]]), "should filter invalid parity wrt wrapping" # not currently implemented so this test is failing




[[1, 2, 3, 4], [5, 2, 3, 4], [2, 3, 4], [2, 1, 5, 4], [3, 2, 1, 5], [4, 3, 2, 1]]

#test_parity_filter()
test_simple_parity_filter()
test_ordering_filter()
test_repeated_step_filter()
test_max_full_length_step_filter()
test_happy_path_filter()
test_lemma_1_filter()
