import unittest
from unittest.mock import MagicMock

from geopy.location import Location
from geopy.point import Point

from propus.geolocator import Geolocator


class TestGeolocator(unittest.TestCase):
    """Tests for Geolocator class"""

    def setUp(self) -> None:
        super().setUp()
        self.geolocator = Geolocator.build(geocoder="testing")
        self.dummy_config = {"api_key": "Authorization some_testing_jwt!"}

        self.address = "1102 Q St Suite 4800, Sacramento, CA 95811, USA"
        self.address_components = [
            {
                "long_name": "Suite 4800",
                "short_name": "Suite 4800",
                "types": ["subpremise"],
            },
            {"long_name": "1102", "short_name": "1102", "types": ["street_number"]},
            {"long_name": "Q Street", "short_name": "Q St", "types": ["route"]},
            {
                "long_name": "Downtown",
                "short_name": "Downtown",
                "types": ["neighborhood", "political"],
            },
            {
                "long_name": "Sacramento",
                "short_name": "Sacramento",
                "types": ["locality", "political"],
            },
            {
                "long_name": "Sacramento County",
                "short_name": "Sacramento County",
                "types": ["administrative_area_level_2", "political"],
            },
            {
                "long_name": "California",
                "short_name": "CA",
                "types": ["administrative_area_level_1", "political"],
            },
            {
                "long_name": "United States",
                "short_name": "US",
                "types": ["country", "political"],
            },
            {"long_name": "95811", "short_name": "95811", "types": ["postal_code"]},
        ]
        self.address_dict = {
            "address1": "1102 Q St",
            "address2": "Suite 4800",
            "city": "Sacramento",
            "state": "CA",
            "zip": "95811",
            "country": "US",
        }
        self.lat_long = "38.5718462, -121.495020"
        self.lat_long_dict = {"latitude": 38.5718462, "longitude": -121.495020}
        self.lat_long_list = [38.5718462, -121.495020]
        self.lat_long_tuple = (38.5718462, -121.495020)

        self.test_name = None
        self.location_object = Location(
            address=self.address,
            point=Point(38.5718462, -121.495020, 0),
            raw={"address_components": self.address_components},
        )
        self.not_implemented_geocoder = "Foo-bar"

    def _make_request(self):
        if "failed" in self.test_name:
            response = None
        else:
            response = self.location_object

        return response

    def test_get_address(self):
        """test_get_address: geocoding and parsing an address string"""
        self.test_name = "get_address"
        self.geolocator.geocoder.geocode = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator.get(self.address), self.address_dict)

    def test_private_get_address(self):
        """test_private_get_address: geocoding an address string"""
        self.test_name = "_get_address"
        self.geolocator.geocoder.geocode = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator._get(self.address), self.location_object)

    def test_reverse(self):
        """test_reverse: reverse geocoding and parsing an coordinates string"""
        self.test_name = "reverse"
        self.geolocator.geocoder.reverse = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator.reverse(self.lat_long), self.address_dict)

    def test_private_reverse(self):
        """test_private_reverse: reverse geocoding an coordinates string"""
        self.test_name = "_reverse"
        self.geolocator.geocoder.reverse = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator._reverse(self.lat_long), self.location_object)

    def test_reverse_dict(self):
        """test_reverse_dict: reverse geocoding and parsing an coordinates dictionary"""
        self.test_name = "reverse_dict"
        self.geolocator.geocoder.reverse = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator.reverse(self.lat_long_dict), self.address_dict)

    def test_private_reverse_dict(self):
        """test_private_reverse_dict: reverse geocoding an coordinates dictionary"""
        self.test_name = "_reverse_dict"
        self.geolocator.geocoder.reverse = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator._reverse(self.lat_long_dict), self.location_object)

    def test_reverse_list(self):
        """test_reverse_list: reverse geocoding and parsing coordinates list"""
        self.test_name = "reverse_list"
        self.geolocator.geocoder.reverse = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator.reverse(self.lat_long_list), self.address_dict)

    def test_private_reverse_list(self):
        """test_private_reverse_list: reverse geocoding coordinates list"""
        self.test_name = "_reverse_list"
        self.geolocator.geocoder.reverse = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator._reverse(self.lat_long_list), self.location_object)

    def test_reverse_tuple(self):
        """test_reverse_tuple: reverse geocoding and parsing coordinates tuple"""
        self.test_name = "reverse_tuple"
        self.geolocator.geocoder.reverse = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator.reverse(self.lat_long_tuple), self.address_dict)

    def test_private_reverse_tuple(self):
        """test_private_reverse_tuple: reverse geocoding coordinates tuple"""
        self.test_name = "_reverse_tuple"
        self.geolocator.geocoder.reverse = MagicMock(return_value=self._make_request())
        self.assertEqual(self.geolocator._reverse(self.lat_long_tuple), self.location_object)

    def test_format_location(self):
        """test_format_location: formatting an address string from raw geocoding address elements"""
        self.test_name = "format_location"
        self.assertEqual(self.geolocator.format_location(self.location_object), self.address_dict)

    def test_geocoder_not_implemented(self):  # Broken
        """test_geocoder_not_implemented: building a geocoder that is not implemented"""
        self.test_name = "geocoder_not_implemented"
        with self.assertRaises(NotImplementedError):
            Geolocator.build(geocoder=self.not_implemented_geocoder, config=self.dummy_config)

    def test_validate(self):
        """test_validate: validating an address success"""
        self.test_name = "validate_true"
        self.geolocator.geocoder.geocode = MagicMock(return_value=self._make_request())
        self.assertTrue(self.geolocator.validate(self.address))

    def test_validate_failed(self):
        """test_validate_failed: validating an address failure"""
        self.test_name = "validate_failed"
        self.geolocator.geocoder.geocode = MagicMock(return_value=self._make_request())
        self.assertFalse(self.geolocator.validate(self.address))


if __name__ == "__main__":
    TestGeolocator.main()
