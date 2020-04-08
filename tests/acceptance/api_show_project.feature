Feature: show index page with some selected projects

  Scenario: show the projects with most downloads from yesterday
    Given the pepy project with the following downloads
      | date       | version | downloads |
      | 2018-05-01 | 1.0     | 10        |
      | 2018-05-02 | 2.0     | 15        |
      | 2018-05-03 | 1.0     | 20        |
      | 2018-05-03 | 2.0     | 20        |
    When I send the GET request to /api/projects/pepy
    Then the response status code should be 200
    And the api response should be
    """
      {
        "id": "pepy",
        "total_downloads": 65,
        "downloads": {
          "2018-05-03": 40,
          "2018-05-02": 15,
          "2018-05-01": 10
        }
      }
    """

  Scenario: show 404 when project not found
    When I send the GET request to /api/projects/pepy
    Then the response status code should be 404
    And the api response should be
    """
      {
        "error": 404,
        "message": "Project with name pepy does not exist"
      }
    """