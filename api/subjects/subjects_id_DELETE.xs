// Delete a subject belonging to the authenticated user
query "subjects/{id}" verb=DELETE {
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

    db.del subjects {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {success: true, message: "Subject successfully deleted."}
  tags = ["edutrack:academic"]
  guid = "c7YPhimrp2B_LVBPeci-Vro1xi0"
}
