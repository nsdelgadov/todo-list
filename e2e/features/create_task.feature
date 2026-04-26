Feature: Creating a new task
  As a user
  I want to add a task to my list

  Scenario: A new task appears in the list after submission
    Given there are no tasks
    When I open the app
    And I type "Buy bread" in the new task input
    And I click "Add"
    Then I see "Buy bread" displayed as not done

  Scenario: Submitting a title longer than 200 characters surfaces the backend error
    Given there are no tasks
    When I open the app
    And I type a title with 201 characters in the new task input
    And I click "Add"
    Then I see "Ensure this field has no more than 200 characters."

  Scenario: Typing past the limit truncates and warns inline
    Given there are no tasks
    When I open the app
    And I type a title with 250 characters in the new task input
    Then the new task input contains 201 characters
    And I see "Max 200 characters"
    When I shorten the new task input to 200 characters
    Then I do not see "Max 200 characters"
