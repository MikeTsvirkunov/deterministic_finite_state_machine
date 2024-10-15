Feature: Test multy rule
  
    Scenario: Test multy rule if all const true rules
        Given Data for multy rule.
        And List of only const True rules for multy rule.
        And Multy rule with setted list of rules.
        When Calling multy rule.
        Then Have been gotted True resulte. 
        Then All rules been called.


    Scenario: Test multy rule if all const false rules
        Given Data for multy rule.
        And List of only const False rules for multy rule.
        And Multy rule with setted list of rules.
        When Calling multy rule.
        Then Have been gotted False resulte. 
        Then All rules been called.

    
    Scenario: Test multy rule if all const false rules
        Given Data for multy rule.
        And List of mix bool const rules for multy rule.
        And Multy rule with setted list of rules.
        When Calling multy rule.
        Then Have been gotted False resulte. 
        Then All rules been called.
