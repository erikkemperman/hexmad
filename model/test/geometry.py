
import unittest

from model import geometry


class TestGeometry(unittest.TestCase):

    RINGS = 12

    def test_assert_polar(self):
        with self.assertRaises(ValueError) as context:
            geometry.assert_polar(-1)
        self.assertTrue('Illegal co-ordinates' in str(context.exception))

        try:
            self.assertFalse(geometry.assert_polar(-1, exception=False))
        except ValueError as exception:
            self.fail('Unexpected exception %s' % str(exception))

        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(-1, 7):
                for t in range(-1, r + 1):
                    if s < 0 or s >= 6 or t < 0 or t >= r:
                        self.assertFalse(geometry.assert_polar(r, s, t, exception=False))
                    else:
                        self.assertTrue(geometry.assert_polar(r, s, t, exception=False))

    def test_assert_index(self):
        with self.assertRaises(ValueError) as context:
            geometry.assert_index(-1)
        self.assertTrue('Illegal index' in str(context.exception))

        try:
            self.assertFalse(geometry.assert_index(-1, exception=False))
        except ValueError as exception:
            self.fail('Unexpected exception %s' % str(exception))

        self.assertFalse(geometry.assert_index(-1, 0, exception=False))
        self.assertTrue(geometry.assert_index(0, 0, exception=False))
        self.assertFalse(geometry.assert_index(1, 0, exception=False))

        for r in range(1, TestGeometry.RINGS):
            lo = 3 * r * (r - 1) + 1
            hi = 3 * r * (r + 1) + 1
            for x in range(lo - 1, hi + 1):
                if x < lo or x >= hi:
                    self.assertFalse(geometry.assert_index(x, r, exception=False))
                else:
                    self.assertTrue(geometry.assert_index(x, r, exception=False))

    def test_index(self):
        x = 0
        self.assertEqual(geometry.index(0, 0, 0), 0, 'index(0, 0, 0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    self.assertEqual(geometry.index(r, s, t), x, 'index(%d, %d, %d)' % (r, s, t))

    def test_ring(self):
        x = 0
        self.assertEqual(geometry.ring(0), 0, 'ring(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    self.assertEqual(geometry.ring(x), r, 'ring(%d)' % x)

    def test_segment(self):
        x = 0
        self.assertEqual(geometry.segment(0), 0, 'segment(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    self.assertEqual(geometry.segment(x), s, 'segment(%d)' % x)

    def test_tranche(self):
        x = 0
        self.assertEqual(geometry.tranche(0), 0, 'tranche(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    self.assertEqual(geometry.tranche(x), t, 'tranche(%d)' % x)

    def test_polar(self):
        x = 0
        self.assertEqual(geometry.polar(0), (0, 0, 0), 'polar(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    self.assertEqual(geometry.polar(x), (r, s, t), 'polar(%d)' % x)

    def test_lateral_prev_index(self):
        x = 0
        self.assertEqual(geometry.lateral_prev_index(0), [], 'lateral_prev_index(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    p = geometry.lateral_prev_index(x)
                    if s == 0 and t == 0:
                        self.assertEqual(p, [x + 6 * r - 1], 'lateral_prev_index(%d)' % x)
                    else:
                        self.assertEqual(p, [x - 1], 'lateral_prev_index(%d)' % x)

    def test_lateral_next_index(self):
        x = 0
        self.assertEqual(geometry.lateral_next_index(0), [], 'lateral_next_index(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    n = geometry.lateral_next_index(x)
                    if s == 5 and t == r - 1:
                        self.assertEqual(n, [x - 6 * r + 1], 'lateral_next_index(%d)' % x)
                    else:
                        self.assertEqual(n, [x + 1], 'lateral_next_index(%d)' % x)

    def test_lateral_index(self):
        x = 0
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    p = geometry.lateral_prev_index(x)
                    self.assertEqual([x], geometry.lateral_next_index(p[0]), 'lateral_index#1(%d)' % x)
                    n = geometry.lateral_next_index(x)
                    self.assertEqual([x], geometry.lateral_prev_index(n[0]), 'lateral_index#2(%d)' % x)
                    self.assertEqual(len(p) + len(n), 2, 'lateral_index#3(%d)' % x)

    def test_radial_prev_index(self):
        x = 0
        self.assertEqual(geometry.radial_prev_index(0), [], 'radial_prev_index(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    p = geometry.radial_prev_index(x)
                    y = x - 6 * (r - 1) - s
                    if r == 1:
                        self.assertEqual(p, [0], 'radial_prev_index(%d)' % x)
                    elif t == 0:
                        self.assertEqual(p, [y], 'radial_prev_index(%d)' % x)
                    elif s == 5 and t == r - 1:
                        self.assertEqual(p, [y - 1, y - 6 * (r - 1)], 'radial_prev_index(%d)' % x)
                    else:
                        self.assertEqual(p, [y - 1, y], 'radial_prev_index(%d)' % x)

    def test_radial_next_index(self):
        x = 0
        self.assertEqual(geometry.radial_next_index(0), [1, 2, 3, 4, 5, 6], 'radial_next_index(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    n = geometry.radial_next_index(x)
                    y = x + 6 * r + s
                    if t == 0:
                        if s == 0:
                            self.assertEqual(n, [y + 5 + 6 * r, y, y + 1], 'radial_next_index(%d)' % x)
                        else:
                            self.assertEqual(n, [y - 1, y, y + 1], 'radial_next_index(%d)' % x)
                    else:
                        self.assertEqual(n, [y, y + 1], 'radial_next_index(%d)' % x)

    def test_radial_index(self):
        x = 0
        for y in geometry.radial_next_index(0):
            self.assertIn(0, geometry.radial_prev_index(y), 'radial_index#1(0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    x += 1
                    p = geometry.radial_prev_index(x)
                    for y in p:
                        self.assertIn(x, geometry.radial_next_index(y), 'radial_index#2(%d)' % x)
                    n = geometry.radial_next_index(x)
                    for y in n:
                        self.assertIn(x, geometry.radial_prev_index(y), 'radial_index#3(%d)' % x)
                    self.assertEqual(len(p) + len(n), 4, 'radial_index#4(%d)' % x)

    def test_lateral_prev_polar(self):
        self.assertEqual(geometry.lateral_prev_polar(0, 0, 0), [], 'radial_prev_index(0, 0, 0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    p = geometry.lateral_prev_polar(r, s, t)
                    if t == 0:
                        if s == 0:
                            self.assertEqual(p, [(r, 5, r - 1)], 'lateral_prev_polar(%d, %d, %d)' % (r, s, t))
                        else:
                            self.assertEqual(p, [(r, s - 1, r - 1)], 'lateral_prev_polar(%d, %d, %d)' % (r, s, t))
                    else:
                        self.assertEqual(p, [(r, s, t - 1)], 'lateral_prev_polar(%d, %d, %d)' % (r, s, t))

    def test_lateral_next_polar(self):
        self.assertEqual(geometry.lateral_next_polar(0, 0, 0), [], 'lateral_next_polar(0, 0, 0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    n = geometry.lateral_next_polar(r, s, t)
                    if t == r - 1:
                        if s == 5:
                            self.assertEqual(n, [(r, 0, 0)], 'lateral_next_polar(%d, %d, %d)' % (r, s, t))
                        else:
                            self.assertEqual(n, [(r, s + 1, 0)], 'lateral_next_polar(%d, %d, %d)' % (r, s, t))
                    else:
                        self.assertEqual(n, [(r, s, t + 1)], 'lateral_next_polar(%d, %d, %d)' % (r, s, t))

    def test_lateral_polar(self):
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    p = geometry.lateral_prev_polar(r, s, t)
                    self.assertEqual([(r, s, t)], geometry.lateral_next_polar(*p[0]), 'lateral_polar#1(%d, %d, %d)' % (r, s, t))
                    n = geometry.lateral_next_polar(r, s, t)
                    self.assertEqual([(r, s, t)], geometry.lateral_prev_polar(*n[0]), 'lateral_polar#2(%d, %d, %d)' % (r, s, t))
                    self.assertEqual(len(p) + len(n), 2, 'lateral_polar#3(%d, %d, %d)' % (r, s, t))

    def test_radial_prev_polar(self):
        self.assertEqual(geometry.radial_prev_polar(0, 0, 0), [], 'radial_prev_polar(0, 0, 0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    p = geometry.radial_prev_polar(r, s, t)
                    if r == 1:
                        self.assertEqual(p, [(0, 0, 0)], 'radial_prev_polar(%d, %d, %d)' % (r, s, t))
                    elif t == 0:
                        self.assertEqual(p, [(r - 1, s, 0)], 'radial_prev_polar(%d, %d, %d)' % (r, s, t))
                    elif t == r - 1:
                        self.assertEqual(p, [(r - 1, s, t - 1), (r - 1, 0 if s == 5 else s + 1, 0)], 'radial_prev_polar(%d, %d, %d)' % (r, s, t))
                    else:
                        self.assertEqual(p, [(r - 1, s, t - 1), (r - 1, s, t)], 'radial_prev_polar(%d, %d, %d)' % (r, s, t))

    def test_radial_next_polar(self):
        self.assertEqual(geometry.radial_next_polar(0, 0, 0), [(1, s, 0) for s in range(0, 6)], 'radial_next_polar(0, 0, 0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    n = geometry.radial_next_polar(r, s, t)
                    if t == 0:
                        self.assertEqual(n, [(r + 1, 5 if s == 0 else s - 1, r), (r + 1, s, 0), (r + 1, s, 1)], 'radial_next_polar(%d, %d, %d)' % (r, s, t))
                    else:
                        self.assertEqual(n, [(r + 1, s, t), (r + 1, s, t + 1)], 'radial_next_polar(%d, %d, %d)' % (r, s, t))

    def test_radial_polar(self):
        for rst in geometry.radial_next_polar(0, 0, 0):
            self.assertIn((0, 0, 0), geometry.radial_prev_polar(*rst), 'radial_polar#1(0, 0, 0)')
        for r in range(1, TestGeometry.RINGS + 1):
            for s in range(0, 6):
                for t in range(0, r):
                    p = geometry.radial_prev_polar(r, s, t)
                    for rst in p:
                        self.assertIn((r, s, t), geometry.radial_next_polar(*rst), 'radial_polar#2(%d, %d, %d)' % (r, s, t))
                    n = geometry.radial_next_polar(r, s, t)
                    for rst in n:
                        self.assertIn((r, s, t), geometry.radial_prev_polar(*rst), 'radial_polar#3(%d, %d, %d)' % (r, s, t))
                    self.assertEqual(len(p) + len(n), 4, 'radial_polar#4(%d, %d, %d)' % (r, s, t))


if __name__ == '__main__':
    unittest.main()
