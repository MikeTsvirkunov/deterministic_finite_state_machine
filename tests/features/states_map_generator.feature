Feature: testing state map generator

    Scenario: build states map on 3 stages
        Given that max stage is 3.
        And that min stage is 1.
        Given list of rules:
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
        When building states map by this rules.
        Then been gotted states map:
            |    COMMAND    | 1ST STAGE | 1ST DOORS STATE | 2ND STAGE | 2ND DOORS STATE |
            |   move_up     |     1     |      closed     |     2     |      closed     |
            |   open_doors  |     1     |      closed     |     1     |      opened     |
            |   close_doors |     1     |      opened     |     1     |      closed     |
            |   move_up     |     2     |      closed     |     3     |      closed     |
            |   move_down   |     2     |      closed     |     1     |      closed     |
            |   open_doors  |     2     |      closed     |     2     |      opened     |
            |   close_doors |     2     |      opened     |     2     |      closed     |
            |   move_down   |     3     |      closed     |     2     |      closed     |
            |   open_doors  |     3     |      closed     |     3     |      opened     |
            |   close_doors |     3     |      opened     |     3     |      closed     |
