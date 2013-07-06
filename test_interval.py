from interval import NullInterval, Interval

def test():
    i1 = Interval(1, 5, None)
    try:
        Interval(2, 1, None)
    except ValueError:
        assert True

    assert len(set((i1, i1)))==1

    assert len(i1)==4
    assert 2 in i1
    assert 0 not in i1
    assert 1 not in i1
    i2 = Interval(1, 5, 'b')
    assert 1 in i2
    assert 2 in i2
    assert 5 in i2
    assert 6 not in i2

    assert i2 in i2
    assert Interval(0, 2, None) not in i2
    assert Interval(1, 4, 'b') in i2
    assert Interval(1, 4, 'r') in i2
    assert Interval(1, 7, 'l') not in i2
    assert Interval(2, 5, None) in i2
    assert Interval(2, 7, None) not in i2
    assert Interval(1, 5, 'b') == i2
    assert Interval(1, 5, 'b') is i2
    assert Interval(1, 5, 'b') != i1

    try:
        Interval('e', 5, None)
    except TypeError:
        assert True

    i1 = Interval(1, 5, None)
    assert repr(i1)=='(1, 5)'
    i2 = Interval(2, 7, None)
    i3 = Interval(1, 7, None)
    assert i1 + i2 == i3
    assert i2 + i1 == i3
    i2 = Interval(6, 8, None)
    try:
        i1 + i2
    except ValueError:
        assert True

    i4 = Interval(8, 9, None)
    try:
        i4 + i2
    except ValueError:
        assert True

    i2 = Interval(2, 5, 'b')
    assert repr(i2)=='[2, 5]'
    i3 = Interval(1, 5, 'r')
    assert i1 + i2 == i3
    i2 = Interval(1, 4, 'l')
    i3 = Interval(1, 5, 'l')
    assert i1 + i2 == i3
    i2 = Interval(2, 4, 'b')
    assert i1 + i2 == i1

    assert Interval(1, 2, None)+i2 == Interval(1, 4, 'r')

    i0 = NullInterval()
    assert i0 is NullInterval()
    assert i0 == NullInterval()
    assert i0 is Interval(1, 1, None)
    assert i0 != i1

    assert len(set((i0, i0)))==1
    assert i0 in i0
    assert 1 not in i0
    assert i1 not in i0

if __name__=='__main__':
    print 'Running tests...'
    test()
