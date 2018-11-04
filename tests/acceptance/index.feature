Feature: show index page with some selected projects

  Scenario: show the projects with most downloads from yesterday
    Given the following projects exists
      | name     | downloads |
      | pepy     | 100       |
      | climoji  | 200       |
      | requests | 300       |
    And the following downloads per day exists
      | name     | date       | downloads |
      | pepy     | 2018-10-01 | 10        |
      | climoji  | 2018-10-01 | 20        |
      | requests | 2018-10-01 | 30        |
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
                <th scope="row"><a href="/project/requests">requests</a></th>
                <td>300</td>
            </tr>
            <tr>
                <th scope="row"><a href="/project/climoji">climoji</a></th>
                <td>200</td>
            </tr>
            <tr>
                <th scope="row"><a href="/project/pepy">pepy</a></th>
                <td>100</td>
            </tr>
        </tbody>
      </table>
    """
