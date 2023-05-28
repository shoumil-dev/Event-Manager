For the purpose of testing the MyEventManager application the following strategies were used to curate test cases that fulfil the testing of the entire application. Parts of the application that requires connection to the google calendar api will be tested using the mocking features that are offered with the pyunit module in python. This will avoid changes made to the actual calendar during testing. Additionally api calls are unreliable and slow and hence using the mocking features will create a better testing experience.

  

# Black Box Testing

  

## Equivalence Partitioning and Boundary Value Analysis

From the tool sets available in black box testing only Equivalence partitioning and Boundary value analysis was used. These two sets were used to create certain test cases for different methods of the application. Using equivalence partitioning the inputs to a certain method can be partitioned based on the requirements of the method. This will allow the splitting of the inputs into valid and invalid inputs to test the methods in the application. For example, a method is supposed to only take integer values as the input. So this would be valid input to the method. However, passing in a value that is not of type integer should be invalid and hence the units/methods should trigger an error. Boundary value analysis will also be used to test for methods/requirements that involve limits or ranges. For example, the MyEventManager application should only allow a maximum of 20 attendees per event. So using boundary values analysis we can create test cases to inspect the boundaries of the method/program and infer whether they follow the requirements or not.

  

Random testing will not be used as it is considered to be unnecessary for the testing of the MyEventManager application. The same goes to category partitioning and combinatorial testing.

  

# White Box Testing

  

## Statement Coverage

Statement coverage will be used as part of the unit testing. This will allow us to cover all the statements in the methods. This strategy will be used for simple methods that only have simple statements that are executed in an order and there are no complicated branching structures like looping and conditional statements.

  

## Branch Coverage/Condition Coverage

Branch coverage will also be exercised in the testing of the application. Branch coverage requires that every if statement or condition in the code must evaluate to true and false at least once in the test cases. This will be used with methods of the application that have conditions such as a while loop or an if statement. So the condition of the while loop and the if statements must result in true or false a minimum of once in the test cases that we create.

  

## Path Coverage

In this testing strategy we will exercise every path through the method as in some cases the previously mentioned strategies do not cover all path combinations. Testing will be done to meet the path coverage criteria using the coverage tool in python.
