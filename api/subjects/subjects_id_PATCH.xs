// Update a subject belonging to the authenticated user
query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
    text? name filters=trim
    text? teacher filters=trim
    int? hours
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

    db.patch subjects {
      field_name = "id"
      field_value = $input.id
      data = {
        name: $input.name
        teacher: $input.teacher
        hours: $input.hours
      }
    } as $updated_subject
  }

  response = $updated_subject
  tags = ["edutrack:academic"]
  guid = "snDJajdyW41fmQV0tYDkWWEl9hI"
}
