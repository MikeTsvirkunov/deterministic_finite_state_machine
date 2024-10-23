Feature: is current stage equal to start stage checker
  
    Scenario Outline: Check does request have same direction with elevator
        Given Elevator with current stage.
        And Request that having start stage <position> than current elevator stage.
        When Calling is_current_stage_equal_to_start_stage_checker.
        Then Have been gotted <expected_result> resulte.

        Examples:
        |  position   | expected_result |
        |    lower    |       False     |
        |    higher   |       False     |
        |    equal    |       True      |