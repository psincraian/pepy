Feature: show index page with some selected projects

  Scenario: show the projects with most downloads from yesterday
    Given the following projects exists
      | name | downloads |
      | pepy | 100       |
    When I send the GET request to /api/projects
    Then the response status code should be 200
    And the api response should be
    """
      [
        {
          "id": "pepy",
          "total_downloads": 100
        }
      ]
    """
