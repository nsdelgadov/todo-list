Feature: Creating a new task
  As a user
  I want to add a task to my list

  Scenario: A new task appears in the list after submission
    Given there are no tasks
    When I open the app
    And I type "Buy bread" in the new task input
    And I click "Add"
    Then I see "Buy bread" displayed as not done
