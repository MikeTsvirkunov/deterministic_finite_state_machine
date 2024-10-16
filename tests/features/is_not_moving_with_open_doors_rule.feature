Feature: Test is not moving with open doors rule
  
    Scenario: Elevator does not change own state
        Given Current stage.
        And Next stage is equal to current stage.
        And Door is opened in current state.
        And Next door state is equal to current state.
        And Current state.
        And Next state.
        When Calling is not moving with open doors rule.
        Then Have been gotted True resulte.


    Scenario: Elevator change stage with opened doors
        Given Current stage.
        And Next stage is not equal to current stage.
        And Door is opened in current state.
        And Next door state is equal to current state.
        And Current state.
        And Next state.
        When Calling is not moving with open doors rule.
        Then Have been gotted False resulte.
    

    Scenario: Elevator change stage with closed doors
        Given Current stage.
        And Next stage is not equal to current stage.
        And Door is closed in current state.
        And Next door state is equal to current state.
        And Current state.
        And Next state.
        When Calling is not moving with open doors rule.
        Then Have been gotted True resulte.
    

    Scenario: Elevator open doors on one stage
        Given Current stage.
        And Next stage is equal to current stage.
        And Door is closed in current state.
        And Next door state is not equal to current state.
        And Current state.
        And Next state.
        When Calling is not moving with open doors rule.
        Then Have been gotted True resulte.
    

    Scenario: Elevator close doors on one stage
        Given Current stage.
        And Next stage is equal to current stage.
        And Door is opened in current state.
        And Next door state is not equal to current state.
        And Current state.
        And Next state.
        When Calling is not moving with open doors rule.
        Then Have been gotted True resulte.


    Scenario: Elevator closing doors and changing stage
        Given Current stage.
        And Next stage is not equal to current stage.
        And Door is opened in current state.
        And Next door state is not equal to current state.
        And Current state.
        And Next state.
        When Calling is not moving with open doors rule.
        Then Have been gotted False resulte.


    Scenario: Elevator opening doors and changing stage
        Given Current stage.
        And Next stage is not equal to current stage.
        And Door is closed in current state.
        And Next door state is not equal to current state.
        And Current state.
        And Next state.
        When Calling is not moving with open doors rule.
        Then Have been gotted False resulte.
