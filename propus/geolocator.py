from typing import AnyStr, Dict, Iterable, Union

from geopy import get_geocoder_for_service

from propus.logging_utility import Logging


class Geolocator:
    def __init__(self, geocoder, config):
        if geocoder.lower() not in ["googlev3", "nominatim"]:
            # Geolocator is configured for GoogleV3
            # Nominatim is for automated testing only
            raise NotImplementedError(f"Geolocator is not implemented for geocoder: {geocoder}.")

        cls = get_geocoder_for_service(geocoder)
        self.geocoder = cls(**config)
        self.name = geocoder
        self.logger = Logging.get_logger("propus/geolocator")

    def __str__(self):
        return f"<Geolocator: {self.name}>"

    @staticmethod
    def build(geocoder: AnyStr = "GoogleV3", config: Dict = {}):
        """
        Singleton to build a geopy geolocator.
        Documentation: https://geopy.readthedocs.io/en/stable/#module-geopy.geocoders
        Args:
            geocoder (AnyStr): Geocoding service to use
               - Defaults to GoogleV3
            config (Dict): Configuration dictionary for the geocoder
                - Defaults to google_maps AWS SSM config

        Returns:
            An instance of Geolocator Class
        """
        if geocoder.lower() == "testing":
            geocoder = "Nominatim"
            config = {"user_agent": "calbright_dev"}
        if not config:
            from propus.aws.ssm import AWS_SSM

            ssm = AWS_SSM.build()
            config = ssm.get_param(parameter_name="google_maps.propus.stage", param_type="json")
        return Geolocator(geocoder, config)

    def format_location(self, location: object) -> Dict:
        """Takes GeoPy / GoogleV3 Location object, and returns dict using internal db naming.
        Documentation: https://developers.google.com/maps/documentation/javascript/geocoding#GeocodingAddressTypes

        Args:
            GeoPy Location object

        Returns:
            Address dictionary, e.g.,
            {
                'address1': '1102 Q St',
                'address2': 'Suite 4800',
                'city': 'Sacramento',
                'state': 'CA',
                'zip': '95811',
                'country': 'US',
            }
        """
        if not location:
            return {}

        street_address = street_number = route = premise = subpremise = floor = room = post_box = city = state = zip = (
            country
        ) = ""
        address_components = location.raw.get("address_components")

        for address_element in address_components:
            if address_element.get("types") == ["street_address"]:
                street_address = address_element.get("short_name")
            elif address_element.get("types") == ["street_number"]:
                street_number = address_element.get("short_name")
            elif address_element.get("types") == ["route"]:
                route = address_element.get("short_name")
            elif address_element.get("types") == ["premise"]:
                premise = address_element.get("short_name")
            elif address_element.get("types") == ["subpremise"]:
                subpremise = address_element.get("short_name")
            elif address_element.get("types") == ["floor"]:
                floor = address_element.get("short_name")
            elif address_element.get("types") == ["room"]:
                room = address_element.get("short_name")
            elif address_element.get("types") == ["post_box"]:
                post_box = address_element.get("short_name")
            elif address_element.get("types") == ["locality", "political"]:
                city = address_element.get("short_name")
            elif address_element.get("types") == [
                "administrative_area_level_1",
                "political",
            ]:
                state = address_element.get("short_name")
            elif address_element.get("types") == ["postal_code"]:
                zip = address_element.get("short_name")
            elif address_element.get("types") == ["country", "political"]:
                country = address_element.get("short_name")

        address_1 = street_address if street_address else " ".join([street_number, route]).strip()
        _address_2 = " ".join([premise, subpremise, floor, room, post_box]).strip()
        address_2 = _address_2 if _address_2 != "" else None
        address_dict = {
            "address1": address_1,
            "address2": address_2,
            "city": city,
            "state": state,
            "zip": zip,
            "country": country,
        }
        return address_dict

    def _get(self, query: AnyStr = None, **kwargs) -> object:
        """_get is a wrapper for the Geopy geocode method
        Documentation: https://geopy.readthedocs.io/en/stable/#geopy.geocoders.GoogleV3.geocode
        Args:
            query: Address to lookup, e.g.,
                '1102 Q St. Suite 4800 Sacramento, CA 95811'

        Returns:
            Geopy Location object, e.g.,
                location.address = '1102 Q St Suite 4800, Sacramento, CA 95811, USA',
                location.point = Point(38.5718462, -121.4950205, 0.0),
                location.raw = {
                    'address_components': [
                        {'long_name': '1102', 'short_name': '1102', 'types': ['street_number']},
                        {'long_name': 'Q Street', 'short_name': 'Q St', 'types': ['route']},
                        [...],
                    ],
                    'formatted_address': '1102 Q St Suite 4800, Sacramento, CA 95811, USA',
                    [...],
                }
        """
        try:
            location_object = self.geocoder.geocode(query=query, **kwargs)
        except Exception as e:
            self.logger.error(f"Geolocator error geocoding {query} ({e})")
            location_object = None

        return location_object

    def get(self, query: AnyStr = None, **kwargs) -> Dict:
        """Uses wrapper for GeoPy geocode / _get function, and then returns a formatted address dictionary
        Documentation: https://developers.google.com/maps/documentation/javascript/geocoding#GeocodingAddressTypes
        Args:
            query: Address to lookup, e.g.,
                '1102 Q St. Suite 4800 Sacramento, CA 95811'

        Returns:
            Address dictionary, e.g.,
            {
                'address1': '1102 Q St',
                'address2': 'Suite 4800',
                'city': 'Sacramento',
                'state': 'CA',
                'zip': '95811',
                'country': 'US',
            }
        """
        location_object = self._get(query=query, **kwargs)
        formatted_address = self.format_location(location_object)
        if formatted_address:
            self.logger.info(f"Geolocator.get formatted address {query} to {formatted_address}")
        else:
            self.logger.error(f"Geolocator.get unable to format address {query}")

        return formatted_address

    def _reverse(self, query) -> object:
        """_reverse is a wrapper for the Geopy reverse method
        Documentation: https://geopy.readthedocs.io/en/stable/#geopy.geocoders.GoogleV3.reverse
        Args:
            query: str or iterable with lat / long, e.g.,
                '34, -123' or (34, -123)

        Returns:
            Geopy Location object, e.g.,
                location.address = '1102 Q St Suite 4800, Sacramento, CA 95811, USA',
                location.point = Point(38.5718462, -121.4950205, 0.0)
                location.raw = {
                    'address_components': [
                        {'long_name': '1102', 'short_name': '1102', 'types': ['street_number']},
                        {'long_name': 'Q Street', 'short_name': 'Q St', 'types': ['route']},
                        [...],
                    ],
                    'formatted_address': '1102 Q St Suite 4800, Sacramento, CA 95811, USA',
                    [...],
                }
        """
        try:
            location_object = self.geocoder.reverse(query)
        except Exception as e:
            self.logger.error(f"Geolocator error reverse geocoding {query} ({e})")
            location_object = None

        return location_object

    def reverse(self, query: Union[AnyStr, Iterable]) -> Dict:
        """
        Wrapper for Geopy reverse geocode function.
        Documentation: https://geopy.readthedocs.io/en/stable/#geopy.geocoders.GoogleV3.reverse
        Args:
            lat_long_pair: Coordinates lookup either as a string
            or as an interable, e.g.,
                '38.571741, -121.494970' or [38.571741, -121.494970]

        Returns:
            Address dictionary, e.g.,
            {
                'address1': '1102 Q. St.',
                'address1': 'Ste. 4800',
                'city': 'Sacramento',
                'state': 'CA',
                'zip': '95811',
                'country': 'United States',
            }
        """
        if isinstance(query, dict):
            coordinates = {}
            for k, v in query.items():
                if k.lower() == "latitude":
                    coordinates["latitude"] = v
                elif k.lower() == "longitude":
                    coordinates["latitude"] = v
            _lat_long_pair = (coordinates.get("latitude"), coordinates.get("longitude"))
        elif isinstance(query, str) or (isinstance(query, Iterable) and len(query) == 2):
            _lat_long_pair = query
        else:
            raise ValueError(f"query ({query}) expected string or latitude / longitude iterable.")

        location_object = self._reverse(_lat_long_pair)
        formatted_address = self.format_location(location_object)

        if formatted_address:
            self.logger.info(f"Geolocator.reverse formatted address {query} to {formatted_address}")
        else:
            self.logger.error(f"Geolocator.reverse unable to format address {query}")

        return formatted_address

    def validate(self, query: AnyStr) -> bool:
        """Uses wrapper for GeoPy geocode / _get function for very basic address validation.
        For better validation, Google has a dedicated API that can be implemented:
           https://developers.google.com/maps/documentation/address-validation
        Args:
            query: Address to lookup, e.g.,
                '1102 Q St. Suite 4800 Sacramento, CA 95811'

        Returns:
            Boolean: True (location was returned) or False (location was not returned)
        """
        location = self._get(query)
        return True if location else False
