Feature: show index page with some selected projects

  Scenario: show the projects with most downloads from yesterday
    Given the following projects exists
      | name     | downloads |
      | pepy     | 100       |
    When I send the GET request to /
    Then the response status code should be 200
    And the response should contain
    """
      <table class="table">
        <thead>
          <tr>
              <th>Project</th>
              <th>Downloads</th>
          </tr>
        </thead>
        <tbody>
            <tr>
                <th scope="row"><a href="/project/pepy">pepy</a></th>
                <td>100</td>
            </tr>
        </tbody>
      </table>
    """
