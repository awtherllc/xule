import unittest

from arelle.plugin import xule


class XuleRegistrationTests(unittest.TestCase):
    def setUp(self):
        self.original_validators = xule._xule_validators
        xule._xule_validators = []

    def tearDown(self):
        xule._xule_validators = self.original_validators

    def test_repeated_web_request_registration_is_idempotent(self):
        xule.xuleRegisterValidators("DQC", "edgarRulesetMap.json")
        xule.xuleRegisterValidators("DQC", "edgarRulesetMap.json")

        self.assertEqual(
            [{"name": "DQC", "map_name": "edgarRulesetMap.json"}],
            xule._xule_validators,
        )

    def test_distinct_rule_maps_remain_registered(self):
        xule.xuleRegisterValidators("DQC", "edgarRulesetMap.json")
        xule.xuleRegisterValidators("DQC", "otherRulesetMap.json")
        xule.xuleRegisterValidators("Xule", "xuleRulesetMap.json")

        self.assertEqual(3, len(xule._xule_validators))

    def test_same_gui_flag_registration_is_idempotent(self):
        flag = object()
        xule.xuleRegisterValidators("DQC", "edgarRulesetMap.json", flag)
        xule.xuleRegisterValidators("DQC", "edgarRulesetMap.json", flag)

        self.assertEqual(1, len(xule._xule_validators))

    def test_distinct_gui_flags_remain_registered(self):
        xule.xuleRegisterValidators("DQC", "edgarRulesetMap.json", object())
        xule.xuleRegisterValidators("DQC", "edgarRulesetMap.json", object())

        self.assertEqual(2, len(xule._xule_validators))


if __name__ == "__main__":
    unittest.main()
