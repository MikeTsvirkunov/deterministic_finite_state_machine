Feature: testing state map generator

    Scenario: build states map on 3 stages
        Given that max stage is 3.
        And that min stage is 1.
        Given list of rules:
            IsMovingToAvailableStage
            IsMovingFromAvailableStage
            BranchIsUniqueForStatesMap
            IsClosingDoorsCorrect
            IsOpeningDoorsCorrect
            IsMovingUpCorrect
            IsMovingDownCorrect
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
