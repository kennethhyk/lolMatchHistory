# API Documentation
---
## End Points
---

**api/v1/listNames**
⋅⋅* Type: GET
⋅⋅* Description: Use this Endpoints to get a list of all records

**api/v1/addName**
⋅⋅* Type: POST
⋅⋅* headers: { "Content-Type": "application/json" }
⋅⋅* body: { "summoner_name": "_STRING_" }
⋅⋅* Description: Use this Endpoints to add a new entry in the database, the `creation_date` is auto generated.

**api/v1/updateName**
⋅⋅* Type: PUT
⋅⋅* headers: { "Content-Type": "application/json" }
⋅⋅* body: { "summoner_name": "_STRING_", "new_name": "_STRING_" }
⋅⋅* Description: Use this Endpoints to modify an entry in the database, search by field `summoner_name` and replace with data in `new_name`

**api/v1/deleteName**
⋅⋅* Type: DELETE
⋅⋅* headers: { "Content-Type": "application/json" }
⋅⋅* body: { "summoner_name": "_STRING_" }
⋅⋅* Description: Use this Endpoints to remove an entry in the database, filter by field `summoner_name`

###### Please find domain class in models.py
