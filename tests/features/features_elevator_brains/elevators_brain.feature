Feature: testing state map generator

    Scenario: run elevator brains
        Given that max stage is 3.
        And that min stage is 1.
        Given requests queue:
            [
                {
                    "from_stage": 2,
                    "to_stage": 3,
                    "direction": "up"
                },
                {
                    "from_stage": 2,
                    "to_stage": 1,
                    "direction": "down"
                }
            ]
        Given elevator state map builded by this rules:
            |      cmd      | is doors opened 1 | is doors opened 2 | is moved up | is moved down | is min stage estimate | is max stage estimate | stage delta |
            |  close_doors  |         1         |          0        |      0      |       0       |           1           |            0          |      0      |
            |  close_doors  |         1         |          0        |      0      |       0       |           0           |            1          |      0      |
            |  close_doors  |         1         |          0        |      0      |       0       |           0           |            0          |      0      |
            |  open_doors   |         0         |          1        |      0      |       0       |           1           |            0          |      0      |
            |  open_doors   |         0         |          1        |      0      |       0       |           0           |            1          |      0      |
            |  open_doors   |         0         |          1        |      0      |       0       |           0           |            0          |      0      |
            |  move_up      |         0         |          0        |      1      |       0       |           1           |            0          |      1      |
            |  move_up      |         0         |          0        |      1      |       0       |           0           |            0          |      1      |
            |  move_down    |         0         |          0        |      0      |       1       |           0           |            1          |      1      |
            |  move_down    |         0         |          0        |      0      |       1       |           0           |            0          |      1      |
        Given first elevator:
            {
                "stage": 1,
                "direction": "up",
                "is_doors_opended": "no",
                "task_queue": [
                    {
                        "to stage": 2,
                        "direction": "up"
                    },
                    {
                        "to stage": 3,
                        "direction": "up"
                    }
                ]
            }
        And second elevator:
            {
                "stage": 3,
                "direction": "down",
                "is_doors_opended": "yes",
                "task_queue": []
            }
        Given elevators brains state map:
            | is_doors_opened | is_finit_stage | is_required_stage | direction | elevator_command |
            |        no       |       no       |         no        |     up    |      move_up     |
            |        no       |       no       |         no        |    down   |     move_down    |
            |        yes      |       no       |         no        |    down   |    close_doors   |
            |        yes      |       no       |         no        |     up    |    close_doors   |
            |        no       |       yes      |         yes       |    down   |    open_doors    |
            |        no       |       no       |         yes       |    down   |    open_doors    |
            |        no       |       yes      |         no        |    down   |    open_doors    |
            |        no       |       yes      |         yes       |     up    |    open_doors    |
            |        no       |       no       |         yes       |     up    |    open_doors    |
            |        no       |       yes      |         no        |     up    |    open_doors    |
        When updating elevators states by using DefaultElevatorsBrain.
        Then been gotted first elevator:
            {
                "stage": 2,
                "direction": "up",
                "is_doors_opended": "no",
                "task_queue": [
                    {
                        "to stage": 2,
                        "direction": "up"
                    },
                    {
                        "to stage": 3,
                        "direction": "up"
                    }
                ]
            }
        And been gotted second elevator:
            {
                "stage": 3,
                "direction": "down",
                "is_doors_opended": "no",
                "task_queue": []
            }
        When updating elevators states by using DefaultElevatorsBrain.
        Then been gotted first elevator:
            {
                "stage": 2,
                "direction": "up",
                "is_doors_opended": "yes",
                "task_queue": [
                    {
                        "from stage": 2,
                        "to stage": 3,
                        "direction": "up"
                    },
                    {
                        "to stage": 3,
                        "direction": "up"
                    }
                ]
            }
        And been gotted second elevator:
            {
                "stage": 2,
                "direction": "down",
                "is_doors_opended": "no",
                "task_queue": []
            }
        When updating elevators states by using DefaultElevatorsBrain.
        Then been gotted first elevator:
            {
                "stage": 2,
                "direction": "up",
                "is_doors_opended": "no",
                "task_queue": [
                    {
                        "to stage": 3,
                        "direction": "up"
                    }
                ]
            }
        And been gotted second elevator:
            {
                "stage": 2,
                "direction": "down",
                "is_doors_opended": "yes",
                "task_queue": [
                    {
                        "from_stage": 2,
                        "to stage": 1,
                        "direction": "down"
                    }
                ]
            }
        When updating elevators states by using DefaultElevatorsBrain.
        Then been gotted first elevator:
            {
                "stage": 3,
                "direction": "up",
                "is_doors_opended": "no",
                "task_queue": [
                    {
                        "to stage": 3,
                        "direction": "up"
                    }
                ]
            }
        And been gotted second elevator:
            {
                "stage": 2,
                "direction": "down",
                "is_doors_opended": "no",
                "task_queue": [
                    {
                        "from_stage": 2,
                        "to stage": 1,
                        "direction": "down"
                    }
                ]
            }
        When updating elevators states by using DefaultElevatorsBrain.
        Then been gotted first elevator:
            {
                "stage": 3,
                "direction": "up",
                "is_doors_opended": "yes",
                "task_queue": [
                ]
            }
        And been gotted second elevator:
            {
                "stage": 1,
                "direction": "down",
                "is_doors_opended": "no",
                "task_queue": [
                    {
                        "from_stage": 2,
                        "to stage": 1,
                        "direction": "down"
                    }
                ]
            }
        When updating elevators states by using DefaultElevatorsBrain.
        Then been gotted first elevator:
            {
                "stage": 3,
                "direction": "down",
                "is_doors_opended": "no",
                "task_queue": [
                ]
            }
        And been gotted second elevator:
            {
                "stage": 1,
                "direction": "down",
                "is_doors_opended": "yes",
                "task_queue": [
                ]
            }

