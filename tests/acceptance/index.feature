Feature: show index page with some selected projects

  Scenario: return 200 http status code and show some projects
    Given the following projects exists
      | name | downloads |
      | pepy | 101       |
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
                <th scope="row"><a href="/count/pepy">pepy</a></th>
                <td>101</td>
            </tr>
        </tbody>
      </table>
    """
