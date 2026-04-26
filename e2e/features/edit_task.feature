Feature: Editing a task title
  As a user
  I want to fix typos or rephrase a task without recreating it

  Scenario: Editing a task title persists the change
    Given a task titled "Buy milk" exists and is not done
    When I open the app
    And I click "Edit" for "Buy milk"
    And I type "Buy oat milk" in the edit input
    And I click "Save"
    Then I see "Buy oat milk" displayed as not done
    And "Buy milk" is no longer displayed

  Scenario: Cancelling an edit leaves the title unchanged
    Given a task titled "Walk the dog" exists and is not done
    When I open the app
    And I click "Edit" for "Walk the dog"
    And I type "Bad change" in the edit input
    And I click "Cancel"
    Then I see "Walk the dog" displayed as not done
