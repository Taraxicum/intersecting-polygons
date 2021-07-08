from filters import OrderingFilter, RepeatedStepFilter, MaxFullLengthStepFilter, HappyPathFilter

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

test_ordering_filter()
test_repeated_step_filter()
test_max_full_length_step_filter()
test_happy_path_filter()
