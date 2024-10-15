Feature: Test state container
  
    Scenario: Getting next state
        Given State container that match state_1 with state_2, and state_1 have didn't match to state_3.
        When Getting match state to state_1.
        Then Have been gotted state_2. 
