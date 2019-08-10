from vector import vector
from visual import vector as visual_vector
import unittest

class TestVectorMethods(unittest.TestCase):

    v0 = visual_vector(0, 0, 0)
    v1 = visual_vector(1, 2, 3)
    v2 = visual_vector(-3, -2, -1)
    visual = [v0, v1, v2]

    vt0 = vector(0, 0, 0)
    vt1 = vector(1, 2, 3)
    vt2 = vector(-3, -2, -1)

    myclass = [vt0, vt1, vt2]

    # round because visual return more decimals than my vector class

    def test_mag(self):
        print('test_mag')
        for v, mc in zip(self.visual, self.myclass):
            self.assertEqual(v.mag, mc.mag())

    def test_mag2(self):
        print('test_mag2')
        for v, mc in zip(self.visual, self.myclass):
            self.assertEqual(v.mag2, mc.mag2())

    def test_norm(self):
        print('test_norm')
        for v, mc in zip(self.visual, self.myclass):
            self.assertEqual(v.norm(), mc.norm())

    def test_add(self):
        print('test_add')
        for i in range(len(self.visual) -1):
            for j in range(len(self.visual)):
                v_add = self.visual[i] + self.visual[j]
                mc_add = self.myclass[i] + self.myclass[j]
                self.assertEqual(v_add, mc_add)

    def test_sub(self):
        print('test_sub')
        for i in range(len(self.visual) -1):
            for j in range(len(self.visual)):
                v = self.visual[i] - self.visual[j]
                mc = self.myclass[i] - self.myclass[j]
                self.assertEqual(v, mc)

    def test_mul(self):
        print('test_mul')
        for v, mc in zip(self.visual, self.myclass):
            v_aux1 = v * -3
            mc_aux = mc * -3
            self.assertEqual(v_aux1, mc_aux)

    def test_rmul(self):
        print('test_rmul')
        for v, mc in zip(self.visual, self.myclass):
            v_aux1 = -3 * v
            mc_aux = -3 * mc
            self.assertEqual(v_aux1, mc_aux)

    def test_cross(self):
        print('test_cross')
        for i in range(len(self.visual) -1):
            for j in range(len(self.visual)):
                v_add = self.visual[i].cross(self.visual[j])
                mc_add = self.myclass[i].cross(self.myclass[j])
                self.assertEqual(v_add, mc_add)

    def test_dot(self):
        print('test_dot')
        for i in range(len(self.visual) - 1):
            for j in range(len(self.visual)):
                v_add = self.visual[i].dot(self.visual[j])
                mc_add = self.myclass[i].dot(self.myclass[j])
                self.assertEqual(v_add, mc_add)

    def test_equal(self):
        print('test_equal')
        v1 = vector(0, 2, -2)
        v2 = vector(0, 2, -2)
        v3 = vector(0, 2, 0)
        self.assertTrue(v1 == v2)
        self.assertFalse(v1==v3)


if __name__ == '__main__':
    unittest.main()