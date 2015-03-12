import unittest
from calcoli import calcola_ris, BadInputError
from calcoli import calcola_numero_goal as calcola


class TestCalcoloGoalSingolaSquadra(unittest.TestCase):
    # def setUp(self):
    #     unittest.TestCase.setUp(self)

    def test_0_goal(self):
        self.assertEqual(calcola(65.5), 0)

    def test_1_goal(self):
        self.assertEqual(calcola(66.), 1)

    def test_2_goal(self):
        self.assertEqual(calcola(72.), 2)

    def test_autogol(self):
        self.assertEqual(calcola(59.5), -1)

    def test_bad_input_as_string(self):
        self.assertRaises(BadInputError, calcola, '60')

    def test_bad_input_as_int(self):
        self.assertRaises(BadInputError, calcola, 60)

#    def tearDown(self):
#        unittest.TestCase.tearDown(self)


class TestCalcoloRisultato(unittest.TestCase):

    def test_1_0(self):
        self.assertEqual(calcola_ris(66., 65.5), (1, 0))

    def test_1_2(self):
        self.assertEqual(calcola_ris(69., 72.), (1, 2))

    def test_1_0_in_fascia(self):
        self.assertEqual(calcola_ris(64., 60.), (1, 0))

    def test_1_2_in_fascia(self):
        self.assertEqual(calcola_ris(67., 71.), (1, 2))

    def test_1_0_con_autogol(self):
        self.assertEqual(calcola_ris(61., 59.5), (1, 0))

    def test_2_0_con_autogol(self):
        self.assertEqual(calcola_ris(66., 59.5), (2, 0))

    def test_delta_over_10(self):
        self.assertEqual(calcola_ris(66., 76.), (1, 3))


calc_sing_suite = unittest.TestLoader().loadTestsFromTestCase(
    TestCalcoloGoalSingolaSquadra)
calc_ris_suite = unittest.TestLoader().loadTestsFromTestCase(
    TestCalcoloRisultato)

all_tests = unittest.TestSuite([calc_sing_suite, calc_ris_suite, ])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(all_tests)
