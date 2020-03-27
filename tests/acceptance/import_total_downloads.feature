Feature: import total download from csv file

  Scenario: import total downloads from csv file
    Given the climoji project with the following downloads
      | date       | version | downloads |
      | 2018-05-01 | 1.0     | 10        |
      | 2018-05-02 | 2.0     | 15        |
    And the a file named total_downloads.csv with the following content
    """
    project,total_downloads
    climoji,1511
    requests,1000000
    """
    When I run the import_total_downloads with file total_downloads.csv
    Then the following projects should exist
      | project  | total_downloads |
      | climoji  | 1511            |
      | requests | 1000000         |