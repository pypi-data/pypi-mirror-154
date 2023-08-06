# README #

The library contains mainly utility functions that can be accessible by multiple microservices at Pouch. For Instance, 
get_ssm_parameters(), get_secret_key(), send_error_to_slack().

### What is this repository for? ###

All services at Pouch have implemented these functions.
This results in code duplication. So, what if some inner configuration is changed and because of that we have to modify
that function in every service. Better to extract it put and create a library out of it.

* Version - 1.0

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact