Feature: testing state map contain no dublicates rule

    Scenario: on state map without dublicates
        Given some set of not dublicated branches.
        When calling this rule.
        Then gotted True.


    Scenario: on state map with dublicates
        Given some set of branches with dublicates.
        When calling this rule.
        Then gotted False.
