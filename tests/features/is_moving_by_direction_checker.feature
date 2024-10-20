Feature: is moving by direction checker
  
    Scenario Outline: Check does request have same direction with elevator
        Given Elevator with <elevator_direction> direction.
        And Request that is <task_direction> request on qurrent stage.
        When Calling is_moving_by_direction_checker.
        Then Have been gotted <expected_result> resulte.

        Examples:
        | elevator_direction |  task_direction   | expected_result |
        |        up          |        up         |       True      |
        |       down         |       down        |       True      |
        |        up          |       down        |       False     |
        |       down         |        up         |       False     |
