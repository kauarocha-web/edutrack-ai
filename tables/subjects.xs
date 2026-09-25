// Stores academic subjects, assigned teacher, workload hours, and user association
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    text teacher filters=trim
    int hours
  
    // Reference to the authenticated user from the Xano user table.
    int user_id? {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
  ]
}