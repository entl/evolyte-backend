import requests
from typing import Any


class PVGISAPIClient:
    BASE_URL = "https://re.jrc.ec.europa.eu/api/"

    @staticmethod
    def fetch_data(tool: str, params: dict, output_format: str = "json"):
        """
        Fetches data from the PVGIS API.

        :param tool: Name of the PVGIS tool (e.g., "PVcalc", "seriescalc", "tmy").
        :param params: Dictionary of query parameters (e.g., {"lat": 50, "lon": 14}).
        :param output_format: Output format (json, csv, basic, epw). Default is "json".
        :return: API response (parsed JSON or raw data).
        """
        url = f"{PVGISAPIClient.BASE_URL}/{tool}"
        params["outputformat"] = output_format  # Ensure output format is included
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

            if output_format == "json":
                return response.json()  # Parse and return JSON response
            return response.text  # Return raw data for other formats

        except requests.exceptions.RequestException as e:
            return {**response.json(), "error": str(e)}
