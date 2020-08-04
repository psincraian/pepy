Feature: show all data for admins

  Scenario: show all the downloads if the token is present
    Given today is 2018-06-30
    And the pepy project with the following downloads
      | date       | version | downloads |
      | 2018-05-01 | 1.0     | 10        |
      | 2018-05-02 | 2.0     | 15        |
      | 2018-05-03 | 1.0     | 20        |
      | 2018-05-03 | 2.0     | 25        |
      | 2018-05-04 | 2.0     | 50        |
    When I send the GET request to /api/v1/admin/projects/pepy?password=pepyrocks
    Then the response status code should be 200
    And the api response should be
    """
    {
      "id": "pepy",
      "total_downloads": 120,
      "versions": ["1.0", "2.0"],
      "downloads": {
        "2018-05-01": {
          "1.0": 10
        },
        "2018-05-02": {
          "2.0": 15
        },
        "2018-05-03": {
          "1.0": 20,
          "2.0": 25
        },
        "2018-05-04": {
          "2.0": 50
        }
      }
    }
    """

  Scenario: fail to show data if password is not present
    Given today is 2018-06-30
    And the pepy project with the following downloads
      | date       | version | downloads |
      | 2018-05-01 | 1.0     | 10        |
    When I send the GET request to /api/v1/admin/projects/pepy
    Then the response status code should be 401
    And the api response should be
    """
    {
      "error": 401,
      "message": "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required."
    }
    """

  Scenario: fail to show data if password not correct
    Given today is 2018-06-30
    And the pepy project with the following downloads
      | date       | version | downloads |
      | 2018-05-01 | 1.0     | 10        |
    When I send the GET request to /api/v1/admin/projects/pepy?password=wrongpass
    Then the response status code should be 401
    And the api response should be
    """
    {
      "error": 401,
      "message": "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required."
    }
    """