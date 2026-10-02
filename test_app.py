import unittest
from app import shipping_fee


class ShippingFeeTest(unittest.TestCase):
    def test_free_shipping_boundary(self):
        self.assertEqual(shipping_fee(4999), 500)
        self.assertEqual(shipping_fee(5000), 0)
        self.assertEqual(shipping_fee(5001), 0)

    def test_invalid_amount(self):
        for amount in (-1, 1.5, True, "5000"):
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                shipping_fee(amount)


if __name__ == "__main__":
    unittest.main()
