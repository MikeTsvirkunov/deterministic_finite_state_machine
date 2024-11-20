Feature: testing default state map

    Scenario: Init state on correct state map
        Given some set of not dublicated branches.
        When try create default state map.
        Then default state map successfully created.


    Scenario: Init state on state map with dublicates
        Given some set of branches with dublicates.
        When try create default state map.
        Then have been gotted error.


    Scenario: Getting next state
        Given some set of not dublicated branches.
        And some alpha states branch in this set.
        Given default state map.
        When try get next state for alpha state.
        Then have been gotted next state for alpha state.
