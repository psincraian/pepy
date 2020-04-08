Feature: import download stats

  Scenario: import download stats by the given date
    Given the following pypi download stats
      | project | date       | version | downloads |
      | flask   | 2020-03-21 | 2.0.1   | 1000      |
      | pepy    | 2020-03-21 | 2.0.1   | 1000      |
      | pepy    | 2020-03-21 | 2.2.1   | 500       |
    When I run the update_version_downloads command for date 2020-03-21
    And I send the GET request to /api/projects/pepy
    Then the response status code should be 200
    And the api response should be
    """
      {
        "id": "pepy",
        "total_downloads": 1500,
        "downloads": {
          "2020-03-21": 1500
        }
      }
    """