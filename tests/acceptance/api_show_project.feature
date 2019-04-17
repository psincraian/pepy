Feature: show index page with some selected projects

  Scenario: show the projects with most downloads from yesterday
    Given the pepy project with the following downloads
      | date       | downloads |
      | 2018-05-01 | 10        |
      | 2018-05-02 | 15        |
      | 2018-05-03 | 20        |
    When I send the GET request to /api/projects/pepy
    Then the response status code should be 200
    And the api response should be
    """
      {
        "id": "pepy",
        "total_downloads": 45,
        "downloads": {
          "2018-05-03": 20,
          "2018-05-02": 15,
          "2018-05-01": 10
        }
      }
    """
