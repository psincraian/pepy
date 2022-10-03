Feature: check that basic endpoints work correctly 

  Scenario: show 404 when url is not found
    When I send the GET request to /random
    Then the response status code should be 404
    And the api response should be
    """
      {
        "error": 404,
        "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
      }
    """

  Scenario: return 200 when calling health-check
    When I send the GET request to /health-check
    Then the response status code should be 200
    And the api response should be
    """
      {
        "status": "healthy"
      }
    """