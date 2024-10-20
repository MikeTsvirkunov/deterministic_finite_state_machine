Feature: requests tasks queues transfer actor
  
    Scenario: Request was added to elevator task queue
        Given Elevator with current stage and current direction.
        And Request with same direction and same start stage.
        And Not empty requests queue with current request.
        When When calling requests tasks queues transfer actor.
        Then Request has been added to elevator task queue.
        And Request has been deleted from request queue.


    Scenario: Request was not added to elevator task queue, cause different direction 
        Given Elevator with current stage and current direction.
        And Request with different direction and same start stage.
        And Not empty requests queue with current request.
        When When calling requests tasks queues transfer actor.
        Then Elevator task queue was not changed.
        And Request has not been deleted from request queue.


    Scenario: Request was not added to elevator task queue, cause different stages 
        Given Elevator with current stage and current direction.
        And Request with same direction and different start stage.
        And Not empty requests queue with current request.
        When When calling requests tasks queues transfer actor.
        Then Elevator task queue was not changed.
        And Request has not been deleted from request queue.
    

    Scenario: Request was not added to elevator task queue, cause different stages 
        Given Elevator with current stage and current direction.
        And Request with different direction and different start stage.
        And Not empty requests queue with current request.
        When When calling requests tasks queues transfer actor.
        Then Elevator task queue was not changed.
        And Request has not been deleted from request queue.
    

    Scenario: Empty request queue
        Given Elevator with current stage and current direction.
        And Empty requests queue.
        When When calling requests tasks queues transfer actor.
        Then Elevator task queue was not changed.
