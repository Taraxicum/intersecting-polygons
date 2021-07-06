from filters import OrderingFilter, RepeatedStepFilter

def test_ordering_filter():
    f = OrderingFilter
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
    f = RepeatedStepFilter
    assert not f.apply_filter([])
    assert not f.apply_filter([[]])
    assert not f.apply_filter([[1, 2, 3, 4]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 2, 3, 4]])
    assert not f.apply_filter([[1, 2, 3, 4], [1, 2, 4, 3]])
    assert f.apply_filter([[1, 2, 3, 4], [1, 3, 5, 2], [1, 2, 3, 4]])
    assert not f.apply_filter([[2, 3, 4], [2, 3, 4, 5]])
    assert f.apply_filter([[2, 3], [1, 3, 5, 2], [2, 3]])

test_ordering_filter()
test_repeated_step_filter()

