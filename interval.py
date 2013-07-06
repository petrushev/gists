_reg = {}

class NullInterval(object):

    def __new__(cls):
        if hasattr(NullInterval, '_obj'):
            return NullInterval._obj

        new = object.__new__(cls)
        NullInterval._obj = new
        return new

    def __eq__(self, I):
        return self is I

    def __ne__(self, I):
        return self is not I

    def __hash__(self):
        return hash(('Interval', 0))

    def __contains__(self, el):
        return self is el

    def __len__(self):
        return 0

    def __repr__(self):
        return '(null)'

    def __add__(self, I):
        return I


class Interval(object):

    def __new__(cls, l, r, include):
        key = (l, r, include in ('l', 'b'), include in ('r', 'b'))
        if key in _reg:
            return _reg[key]

        if type(l) is not type(r):
            raise TypeError, 'left and right bounds are of different type'

        if l==r and include is None:
            new = NullInterval()
        else:
            new = object.__new__(cls, l, r, include)

        _reg[key] = new
        return new


    def __init__(self, l, r, include):
        if r < l:
            raise ValueError, 'Negative interval length'

        self._l = l
        self._r = r

        # border inclusion flags
        self._incl = include in ('l', 'b') # left
        self._incr = include in ('r', 'b') # right

    def __eq__(self, I):
        return (self._l, self._r, self._incl, self._incr)==(I._l, I._r, I._incl, I._incr)

    def __ne__(self, I):
        return not self==I

    def __hash__(self):
        return hash(('Interval', self._l, self._r, self._incl, self._incr))

    def __contains__(self, el):
        if type(el) is Interval:
            if self._l < el._l:
                if el._r < self._r:
                    return True
                if el._r > self._r:
                    return False
                # el._r == self._r:
                if self._incr or (not el._incr):
                    return True
                return False

            if self._l > el._l:
                return False

            # el._l == self._l
            if self._incl or (not el._incl):
                if el._r < self._r:
                    return True
                if el._r > self._r:
                    return False
                # el._r == self._r: (equal!)
                if self._incr or (not el._incr):
                    return True
                return False

            # fail
            return False

        return (self._l < el and el < self._r) or \
               (self._incl and el==self._l) or (self._incr and el==self._r)

    def __len__(self):
        return self._r - self._l

    def __repr__(self):
        l = '[' if self._incl else '('
        r = ']' if self._incr else ')'
        return '%s%s, %s%s' % (l, repr(self._l), repr(self._r), r)

    def __add__(self, i):
        if i is NullInterval():
            return self
        if i._l < self._l: return i+self # commuted case
        if i._l > self._r:
            raise ValueError, 'intervals are disjoint'

        if self._r == i._l: # 1-point join
            if not (self._incr or i._incl ):
                # neither interval contain border
                raise ValueError, 'intervals are disjoint'

        # left border
        l = self._l

        if i._l==self._l:
            incl = self._incl or i._incl
        else:
            incl = self._incl

        if self._r < i._r:
            r = i._r
            incr = i._incr
        elif self._r == i._r:
            r = self._r
            incr = i._incr or self._incr
        else: # self._r > i._r
            r = self._r
            incr = self._incr

        if incl and incr: inc='b'
        elif incl: inc='l'
        elif incr: inc='r'
        else: inc=None

        return Interval(l, r, inc)
