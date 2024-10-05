#### Sharon Gikenye's Code Challenge
## Instructions
For this assessment, you'll be working on an API for tracking heroes and their superpowers.
Setup
Create a new PRIVATE repository, and add your TM as a collaborator. Push your solution to this repository and submit for grading.
You have been provided a Postman collection Download Postman collection. This collection contains all the endpoints that you are required to create with this API. You can download and import it into your Postman application to test that your app works correctly. 

## Setup
1. Run:
    ``` bash
    pipenv install && pipenv shell
    ```
    to install all dependencies and get into the virtual environment. Then cd ino server directory
2. Configure the FLASK_APP and FLASK_RUN_PORT environment variables:
    ``` bash
    export FLASK_APP=app.py
    export FLASK_RUN_PORT=5555
    ```
3. The migrations were already done using:
    ``` bash
    flask db init
    flask db migrate -m "initial migration"
    flask db upgrade head
    ```
4. Populate the database by running:
    ``` bash
    python seed.py
    ```


## Deliverables
Your job is to build out the Flask API to add the functionality described in the deliverables below.

### Models
- A `Hero` has many `Power`s through `HeroPower`
- A `Power` has many `Hero`s through `HeroPower`
- A `HeroPower` belongs to a `Hero` and belongs to a `Power`

Since a `HeroPower` belongs to a `Hero` and a `Power`, configure the model to cascade deletes.

Set serialization rules to limit the recursion depth.
Run the migrations and seed the database
If you aren't able to get the provided seed file Download seed fileworking, you are welcome to generate your own seed data to test the application.

### Validations

Add validations to the `HeroPower` model:

- `strength` must be one of the following values: 'Strong', 'Weak', 'Average'

Add validations to the `Power` model:

- `description` must be present and at least 20 characters long

### Routes

Set up the following routes. Make sure to return JSON data in the format specified along with the appropriate HTTP verb.

Recall you can specify fields to include or exclude when serializing a model instance to a dictionary using to_dict() (don't forget the comma if specifying a single field).

#### a. GET /heroes
Return JSON data of all heroes.
``` bash
[
 {
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel"
 },
 {
  "id": 2,
  "name": "Doreen Green",
  "super_name": "Squirrel Girl"
 },
 {
  "id": 3,
  "name": "Gwen Stacy",
  "super_name": "Spider-Gwen"
 },
 {
  "id": 4,
  "name": "Janet Van Dyne",
  "super_name": "The Wasp"
 },
 {
  "id": 5,
  "name": "Wanda Maximoff",
  "super_name": "Scarlet Witch"
 },
 {
  "id": 6,
  "name": "Carol Danvers",
  "super_name": "Captain Marvel"
 },
 {
  "id": 7,
  "name": "Jean Grey",
  "super_name": "Dark Phoenix"
 },
 {
  "id": 8,
  "name": "Ororo Munroe",
  "super_name": "Storm"
 },
 {
  "id": 9,
  "name": "Kitty Pryde",
  "super_name": "Shadowcat"
 },
 {
  "id": 10,
  "name": "Elektra Natchios",
  "super_name": "Elektra"
 }
]
```

#### b. GET /heroes/:id
If the `Hero` exists, return JSON data.
``` bash
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
     {
       "hero_id": 1,
       "id": 1,
       "power": {
              "description": "gives the wielder the ability to fly through the skies at supersonic speed",
              "id": 2,
              "name": "flight"
        },
       "power_id": 2,
       "strength": "Strong"
        }
   ]
}
```
If the `Hero` does not exist, return the following JSON data, along with the appropriate HTTP status code:
``` bash
    {
        "error": "Hero not found"
    }
```
#### c. GET /powers
Return JSON data in the format below:
``` bash
[
 {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
 },
 {
    "description": "gives the wielder the ability to fly through the skies at supersonic speed",
    "id": 2,
    "name": "flight"
 },
 {
    "description": "allows the wielder to use her senses at a super-human level",
    "id": 3,
    "name": "super human senses"
 },
 {
    "description": "can stretch the human body to extreme lengths",
    "id": 4,
    "name": "elasticity"
 }
]
```

#### d. GET /powers/:id
If the `Power` exists, return JSON data in the format below:
``` bash
{
  "description": "gives the wielder super-human strengths",
  "id": 1,
  "name": "super strength"
}
```

If the `Power` does not exist, return the following JSON data, along with the appropriate HTTP status code:
``` bash
{
  "error": "Power not found"
}
```

#### e. PATCH /powers/:id
This route should update an existing `Power`. It should accept an object with the following properties in the body of the request:
``` bash
{
 "description": "Valid Updated Description"
}
```

If the `Power` exists and is updated successfully (passes validations), update its description and return JSON data in the format below:
``` bash
{
  "description": "Valid Updated Description",
  "id": 1,
  "name": "super strength"
}
```

If the `Power` does not exist, return the following JSON data, along with the
appropriate HTTP status code:
``` bash
{
 "error": "Power not found"
}
```

If the `Power` is **not** updated successfully (does not pass validations), return the following JSON data, along with the appropriate HTTP status code:
``` bash
{
 "errors": ["validation errors"]
}
```

#### f. POST /hero_powers
This route should create a new `HeroPower` that is associated with an existing `Power` and `Hero`. It should accept an object with the following properties in the body of the request:
``` bash
{
 "strength": "Average",
 "power_id": 1,
 "hero_id": 3
}
```
If the `HeroPower` is created successfully, send back a response with the data related to the new `HeroPower`:
``` bash
{
 "id": 11,
 "hero_id": 3,
 "power_id": 1,
 "strength": "Average",
 "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
 },
 "power": {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
 }
}
```
If the `HeroPower` is **not** created successfully, return the following JSON data, along with the appropriate HTTP status code:
``` bash
{
 "errors": ["validation errors"]
}
```
