Feature: show index page with some selected projects

  Scenario: return 200 http status code and show some projects
    Given the pepy project with the following downloads
      | date       | downloads |
      | 2018-05-01 | 10        |
      | 2018-05-02 | 15        |
      | 2018-05-03 | 20        |
    When I send the GET request to /project/pepy
    Then the response status code should be 200
    And the response should contain
    """
      <table class="table">
        <thead>
        <tr>
            <th>Date</th>
            <th>Downloads</th>
        </tr>
        </thead>
        <tbody>
            <tr>
                <td>2018-05-03</td>
                <td>20</td>
            </tr>
            <tr>
                <td>2018-05-02</td>
                <td>15</td>
            </tr>
            <tr>
                <td>2018-05-01</td>
                <td>10</td>
            </tr>
        </tbody>
      </table>
    """
