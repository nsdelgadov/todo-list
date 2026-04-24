Feature: Viewing the task list
  As a user of the app
  I want to see my tasks at a glance with their done state

  Scenario: Tasks are listed with their done state
    Given a task titled "Buy milk" exists and is not done
    And a task titled "Walk the dog" exists and is done
    When I open the app
    Then I see "Buy milk" displayed as not done
    And I see "Walk the dog" displayed as done

  Scenario: An empty task list shows a friendly message
    Given there are no tasks
    When I open the app
    Then I see "No tasks yet"
