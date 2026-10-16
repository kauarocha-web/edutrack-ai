// Get a single subject by ID belonging to the authenticated user
query "subjects/{id}" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
  }

  stack {
    db.query subjects {
      where = ($db.subjects.id == $input.id) && ($db.subjects.user_id == $auth.id)
      return = {type: "single"}
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found or does not belong to the authenticated user."
    }
  }

  response = $subject
  tags = ["edutrack:academic"]
  guid = "e3kurM4AgjmqSAJ_1A6TIHTMypg"
}
