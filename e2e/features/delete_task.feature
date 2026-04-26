Feature: Deleting a task
  As a user
  I want to remove tasks I no longer need

  Scenario: Deleting a task takes two clicks (the first arms confirmation)
    Given a task titled "Old task" exists and is not done
    And a task titled "Keep me" exists and is not done
    When I open the app
    And I click "Delete" for "Old task"
    Then I see "Confirm delete?" for "Old task"
    When I click "Confirm delete?" for "Old task"
    Then "Old task" is no longer displayed
    And I see "Keep me" displayed as not done
