Feature: Toggling a task between done and not done
  As a user
  I want to mark tasks as completed (or undo it)

  Scenario: Marking a pending task as done
    Given a task titled "Buy milk" exists and is not done
    When I open the app
    And I check "Buy milk"
    Then I see "Buy milk" displayed as done

  Scenario: Unmarking a done task
    Given a task titled "Walk the dog" exists and is done
    When I open the app
    And I uncheck "Walk the dog"
    Then I see "Walk the dog" displayed as not done
